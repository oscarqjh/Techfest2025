import type { BaseStorage } from '../base/index.js';
import { createStorage, StorageEnum } from '../base/index.js';

type Data = any;

type DataStorage = BaseStorage<Data> & {
  setData: (value: any) => Promise<void>;
};

const storage = createStorage<Data>(
  'rurl-data',
  {},
  {
    storageEnum: StorageEnum.Local,
    liveUpdate: true,
  },
);

// You can extend it with your own methods
export const dataStorage: DataStorage = {
  ...storage,
  setData: async (value: any) => {
    await storage.set(value);
  },
};
