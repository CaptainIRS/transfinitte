import React from 'react';
import Graph from 'vis-react';
import {
  Center, Button, Tabs, NumberInput, Modal,
  Container, createStyles, Select, TextInput, Title
} from '@mantine/core';
import {
  getAssemblyRequest, getDistrictsRequest, getTreeRequest, getTreesRequest
} from '../../utils/requests';
import { useLoading } from '../../hooks/useLoading';

const useStyles = createStyles((theme) => ({
  root: {
    position: 'relative'
  },

  input: {
    height: 'auto',
    paddingTop: 18
  },

  label: {
    position: 'absolute',
    pointerEvents: 'none',
    fontSize: theme.fontSizes.xs,
    paddingLeft: theme.spacing.sm,
    paddingTop: theme.spacing.sm / 2,
    zIndex: 1
  }
}));

export function LandingPage() {
  const [activeTab, setActiveTab] = React.useState('first');

  const { classes } = useStyles();

  const [states, setStates] = React.useState([]);
  const [state, setState] = React.useState(null);
  const { request } = useLoading();

  React.useEffect(async () => {
    const data = [
      { state_code: 'S06', state_name: 'Gujarat' },
      { state_code: 'S07', state_name: 'Haryana' },
      { state_code: 'S10', state_name: 'Karnataka' },
      { state_code: 'S14', state_name: 'Manipur' },
      { state_code: 'S15', state_name: 'Meghalaya' },
      { state_code: 'S16', state_name: 'Mizoram' },
      { state_code: 'S18', state_name: 'Odisha' },
      { state_code: 'S19', state_name: 'Punjab' },
      { state_code: 'S21', state_name: 'Sikkim' },
      { state_code: 'S22', state_name: 'Tamil Nadu' },
      { state_code: 'S26', state_name: 'Chattisgarh' }
    ];

    setStates(data.map((statu) => ({ label: statu.state_name, value: statu.state_code })));
  }, []);

  const [districts, setDistricts] = React.useState([]);
  const [district, setDistrict] = React.useState(null);

  const getDistricts = async (stateCode) => {
    setState(stateCode);
    const { data } = await request(() => getDistrictsRequest(stateCode));
    setDistricts(data.map((districtu) => ({
      label: districtu.dist_name,
      value: districtu.dist_no
    })));
  };

  const [opened, setOpened] = React.useState(false);
  const [assemblies, setAssemblies] = React.useState([]);
  const [assembly, setAssembly] = React.useState(null);

  const getAssemblies = async (districtCode) => {
    setDistrict(districtCode);
    const { data } = await request(() => getAssemblyRequest(districtCode, state));
    setAssemblies(data.map((assembli) => ({
      label: assembli.ac_name,
      value: assembli.ac_no
    })));
  };

  const [gender, setGender] = React.useState();
  const [date, setDate] = React.useState(new Date());
  const [name, setName] = React.useState('');
  const [fatherName, setFatherName] = React.useState('');

  const [graph, setGraph] = React.useState({});
  const postRequest = async () => {
    const { data } = await request(() => getTreeRequest({
      state,
      district,
      assembly,
      gender,
      dob: date,
      name,
      relativesName: fatherName
    }));
    setOpened(true);
    setGraph(data);
  };

  const [part, setPart] = React.useState();

  const postRequest2 = async () => {
    console.log(part, state, district, assembly);
    const { data } = await request(() => getTreesRequest({
      state,
      district,
      assembly,
      part
    }));
    setOpened(true);
    console.log(data);
    setGraph(data);
  };

  return (
    <>
      <Modal
        opened={opened}
        onClose={() => setOpened(false)}
        title="Tree"
        fullScreen
      >
        <Center>
          <Graph
            style={{ width: '80vw', height: '80vh' }}
            graph={graph}
            options={{
              nodes: {
                borderWidth: 1,
                color: {
                  border: 'grey'
                },
                shape: 'box'
              },
              interaction: { hover: false },
              physics: {
                enabled: true
              },
              edges: {
                color: 'grey'
              }
            }}
          />
        </Center>
      </Modal>
      <Container>
        <Tabs value={activeTab} onTabChange={setActiveTab}>
          <Center>
            <Tabs.List>
              <Tabs.Tab value="first">Individual</Tabs.Tab>
              <Tabs.Tab value="second">Constituency</Tabs.Tab>
            </Tabs.List>
          </Center>
          <Tabs.Panel value="first" p={20}>
            <Center><Title order={3} m="5">Person&#39;s Family Tree Search</Title></Center>
            <TextInput
              m={5}
              label="Name"
              placeholder="Enter Name"
              classNames={classes}
              value={name}
              onChange={(event) => setName(event.currentTarget.value)}
            />

            <TextInput
              m={5}
              label="Father's Name"
              placeholder="Enter Father's Name"
              classNames={classes}
              value={fatherName}
              onChange={(event) => setFatherName(event.currentTarget.value)}
            />

            <Select
              m={5}
              data={states}
              placeholder="Pick one"
              label="Your State"
              classNames={classes}
              onChange={getDistricts}
            />

            <Select
              m={5}
              data={districts}
              placeholder={districts.length ? 'Pick one' : 'Select State First'}
              label="Your District"
              classNames={classes}
              onChange={getAssemblies}
            />

            <Select
              m={5}
              data={assemblies}
              placeholder={assemblies.length ? 'Pick one' : 'Select District First'}
              label="Your Assembly"
              classNames={classes}
              onChange={setAssembly}
            />

            <Select
              m={5}
              data={[
                {
                  value: 'M',
                  label: 'Male'
                },
                {
                  value: 'F',
                  label: 'Female'
                },
                {
                  value: 'O',
                  label: 'Other'
                }
              ]}
              placeholder="Select Your Gender"
              label="Gender"
              classNames={classes}
              onChange={setGender}
            />

            <NumberInput m={5} label="Age" classNames={classes} value={date} onChange={setDate} />
            <Center m={20}>
              <Button onClick={postRequest}>Search</Button>
            </Center>
          </Tabs.Panel>
          <Tabs.Panel value="second" p={20}>
            <Center><Title order={3} m="5">Constituency Family Trees</Title></Center>
            <Select
              m={5}
              data={states}
              placeholder="Pick one"
              label="Select State"
              classNames={classes}
              onChange={getDistricts}
            />

            <Select
              m={5}
              data={districts}
              placeholder={districts.length ? 'Pick one' : 'Select State First'}
              label="Select District"
              classNames={classes}
              onChange={getAssemblies}
            />

            <Select
              m={5}
              data={assemblies}
              placeholder={assemblies.length ? 'Pick one' : 'Select District First'}
              label="Select Assembly"
              classNames={classes}
              onChange={setAssembly}
            />

            <NumberInput
              m={5}
              label="Part Number"
              placeholder="Enter Part Number"
              classNames={classes}
              onChange={setPart}
            />

            <Center m={20}>
              <Button onClick={postRequest2}>Search</Button>
            </Center>
          </Tabs.Panel>
        </Tabs>
      </Container>
    </>
  );
}
