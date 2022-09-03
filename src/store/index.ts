import useExperimentsStore from './experiments'
import useVersionStore from './store'
import useConfigureStore from './config'
// 统一导出useStore方法
export default function useStore() {
  return {
    experiments: useExperimentsStore(),
    version: useVersionStore(),
    config: useConfigureStore()
  }
}