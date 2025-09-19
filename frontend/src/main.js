import { createApp } from "vue";
import { createPinia } from "pinia";
import CarbonVue3 from "@carbon/vue";

import App from "./App.vue";
import router from "./router";

import "carbon-components/css/carbon-components.css";
import "@/styles/globals.scss";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(CarbonVue3);

app.mount("#app");
