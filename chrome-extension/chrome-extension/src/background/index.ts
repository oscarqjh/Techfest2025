import 'webextension-polyfill';
import { exampleThemeStorage } from '@extension/storage';
import { dataStorage } from '@extension/storage';

exampleThemeStorage.get().then(theme => {
  console.log('theme', theme);
});

// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//   if (request.action === 'getStorageData') {
//     chrome.storage.local.get(['scanResult'], data => {
//       sendResponse(data.scanResult || 'No data found');
//     });
//     return true; // Required to make sendResponse async
//   }
//   return;
// });

console.log('Background loaded');
console.log("Edit 'chrome-extension/src/background/index.ts' and save to reload.");
