import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import { MantineProvider, ColorSchemeProvider } from '@mantine/core';
import { NotificationsProvider } from '@mantine/notifications';
import theme from './utils/theme';
import * as serviceWorker from './serviceWorker';
import { LoadingProvider } from './hooks/useLoading';
import { GeneralPageContainer } from './containers/GeneralPageContainer';
import { LandingPage } from './components/LandingPage';

function App() {
  const [colorScheme, setColorScheme] = useState('light');
  const toggleColorScheme = (value) => setColorScheme(value || (colorScheme === 'dark' ? 'light' : 'dark'));
  return (
    <ColorSchemeProvider colorScheme={colorScheme} toggleColorScheme={toggleColorScheme}>
      <MantineProvider
        withNormalizeCSS
        withGlobalStyles
        theme={{
          colorScheme, ...theme
        }}
      >
        <NotificationsProvider>
          <LoadingProvider>
            <GeneralPageContainer child={<LandingPage />} />
          </LoadingProvider>
        </NotificationsProvider>
      </MantineProvider>
    </ColorSchemeProvider>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <App />
);

serviceWorker.register();
