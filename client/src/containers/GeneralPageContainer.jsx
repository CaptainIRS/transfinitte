import React, { useState } from 'react';
import {
  AppShell,
  useMantineTheme, ScrollArea, LoadingOverlay
} from '@mantine/core';
import PropTypes from 'prop-types';
import { HeaderNav } from '../components/Header';
import { useLoading } from '../hooks/useLoading';

export function GeneralPageContainer({ child }) {
  const theme = useMantineTheme();
  const [opened, setOpened] = useState(false);
  const { isLoading } = useLoading();
  return (
    <>
      <LoadingOverlay visible={isLoading} />
      <AppShell
        styles={{
          main: {
            background: theme.colorScheme === 'dark' ? theme.colors.dark[9] : theme.colors.gray[1]
          }
        }}
        navbarOffsetBreakpoint="xs"
        header={
          <HeaderNav opened={opened} setOpened={setOpened} />
        }
      >
        <ScrollArea style={{ height: window.innerHeight - 120 }}>
          {child}
        </ScrollArea>
      </AppShell>
    </>
  );
}

GeneralPageContainer.propTypes = {
  child: PropTypes.element.isRequired
};
