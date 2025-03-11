import { sampleFunction } from '@src/sampleFunction';

console.log('content script loaded');

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getStorageData') {
    chrome.storage.local.get('rurl', data => {
      sendResponse(data || 'No data found');
    });
    return true; // Required to make sendResponse async
  }
  return;
});

// Shows how to call a function defined in another module
sampleFunction();
