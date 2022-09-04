import useExperimentsStore from './experiments'
import {useVersionStore, useDefaultSetting} from './store'
import useConfigureStore from './config'
// 统一导出useStore方法
export default function useStore() {
  return {
    experiments: useExperimentsStore(),
    version: useVersionStore(),
    config: useConfigureStore(),
    settings: useDefaultSetting(),
  }
}