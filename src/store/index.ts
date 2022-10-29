import useExperimentsStore from './experiments'
import { useStatusStore } from './status'
import {useVersionStore, useDefaultSetting} from './store'
// 统一导出useStore方法
export default function useStore() {
  return {
    experiments: useExperimentsStore(),
    version: useVersionStore(),
    settings: useDefaultSetting(),
    status: useStatusStore()
  }
}