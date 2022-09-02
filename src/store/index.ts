import useExperimentsStore from './experiments'
import useVersionStore from './store'

// 统一导出useStore方法
export default function useStore() {
  return {
    experiments: useExperimentsStore(),
    version: useVersionStore(),
  }
}