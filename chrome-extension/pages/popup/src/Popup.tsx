import '@src/Popup.css';
import { useStorage, withErrorBoundary, withSuspense } from '@extension/shared';
import { exampleThemeStorage } from '@extension/storage';
import { t } from '@extension/i18n';
import { AnimatedCircularProgressBar } from '@extension/ui';
import { useState } from 'react';

const notificationOptions = {
  type: 'basic',
  iconUrl: chrome.runtime.getURL('icon-34.png'),
  title: 'Injecting content script error',
  message: 'You cannot inject script here!',
} as const;

const Popup = () => {
  const theme = useStorage(exampleThemeStorage);
  const [url, setUrl] = useState('');
  const [data, setData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const isLight = theme === 'light';
  const logo = isLight ? 'popup/logo.png' : 'popup/logo.png';
  const goGithubSite = () =>
    chrome.tabs.create({ url: 'https://github.com/Jonghakseo/chrome-extension-boilerplate-react-vite' });

  const getCurrentTabUrl = async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab?.url || 'No URL found';
  };

  const handleScan = async () => {
    const [tab] = await chrome.tabs.query({ currentWindow: true, active: true });

    if (tab.url!.startsWith('about:') || tab.url!.startsWith('chrome:')) {
      chrome.notifications.create('inject-error', notificationOptions);
    }

    // set loading state
    setIsLoading(true);

    // get current url
    getCurrentTabUrl().then(async url => {
      // make api call
      let response = await fetch('http://localhost:8000/analyse_credibility', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${process.env.CEB_RENDER_API_KEY}`,
        },
        body: JSON.stringify({ url }),
      });
      let data = await response.json();
      data = JSON.parse(data);
      setData(data);

      setIsLoading(false);
    });
  };

  const handleReset = () => {
    setData(null);
  };

  const handleRedirect = () => {
    chrome.tabs.create({ url: 'http://localhost:3000' });
  };

  return (
    <div className={`App ${isLight ? 'bg-slate-50' : 'bg-gray-800'}`}>
      <header className={`App-header ${isLight ? 'text-gray-900' : 'text-gray-100'}`}>
        {/* <button onClick={goGithubSite}>
          <img src={chrome.runtime.getURL(logo)} className="App-logo" alt="logo" />
        </button>
        <p>
          Edit <code>pages/popup/src/Popup</code>
        </p> */}

        <div className="flex flex-col justify-around items-center w-full h-full">
          {!data && <img src={chrome.runtime.getURL(logo)} className="App-logo" alt="logo" />}

          {isLoading && <div className="spinner"></div>}

          {data && (
            <div>
              <p>80</p>
            </div>
          )}

          {!isLoading && !data && (
            <button
              className={
                'font-bold mb-4 rounded shadow hover:scale-105 p-4' +
                (isLight ? 'bg-blue-200 text-black' : 'bg-gray-800 text-zinc-200')
              }
              onClick={handleScan}>
              Start scanning
            </button>
          )}

          {data && (
            <>
              <div className="flex flex-col justify-center items-center">
                <button
                  className={
                    'font-bold rounded shadow hover:scale-105 p-4' +
                    (isLight ? 'bg-blue-200 text-black' : 'bg-gray-800 text-zinc-200')
                  }
                  onClick={handleRedirect}>
                  See more details
                </button>
                <button
                  className={
                    'font-bold rounded shadow hover:scale-105 p-4' +
                    (isLight ? 'bg-blue-200 text-black' : 'bg-gray-800 text-zinc-200')
                  }
                  onClick={handleReset}>
                  Reset
                </button>
              </div>
            </>
          )}
        </div>
        {/* <ToggleButton>{t('toggleTheme')}</ToggleButton> */}
      </header>
    </div>
  );
};

export default withErrorBoundary(withSuspense(Popup, <div> Loading ... </div>), <div> Error Occur </div>);
