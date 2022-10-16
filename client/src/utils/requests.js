import axios from 'axios';
import {
  GET_STATES,
  GET_DISTRICTS,
  GET_ASSEMBLY,
  GET_CAPTCHA,
  GET_TREE,
  GET_TREES
} from './urls';

// // withCredentials
// const withCredentials = {
//   withCredentials: true
// };

// getStates
export const getStatesRequest = () => axios.get(GET_STATES);

// getDistricts
export const getDistrictsRequest = (stateId) => axios.get(`${GET_DISTRICTS}?state_no=${stateId}`);

// getAssembly
export const getAssemblyRequest = (districtId, stateId) => axios.get(`${GET_ASSEMBLY}?dist_no=${districtId}&state_no=${stateId}`);

// getcaptcha
export const getCaptchaRequest = () => axios.get(GET_CAPTCHA);

// get tree
export const getTreeRequest = ({
  name, relativesName, dob, state, gender, district, assembly
}) => axios.post(`${GET_TREE}?name=${name}&relative_name=${relativesName}&dob=${dob}&state=${
  state
}&gender=${
  gender
}&district=${
  district
}&ac=${
  assembly
}`);

export const getTreesRequest = ({
  state, district, assembly, part
}) => axios.post(`${GET_TREES}?state=${state}&district=${district}&ac=${assembly}&part_no=${part}`);
