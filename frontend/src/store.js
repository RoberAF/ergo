import { reactive } from 'vue';

export const globalState = reactive({
  messages: []
});

export function addMessage(message) {
  globalState.messages.push(message);
}
