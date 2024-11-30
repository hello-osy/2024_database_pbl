/**
 * components 폴더에 있는 컴포넌트 구성 및 내보내기를 관리하는 파일
 * 예시)
 * import components from '@/components/index.js
 * import { 특정 컴포넌트 } from '@/components/index.js
**/
import FormGroupInput from "./Inputs/formGroupInput.vue";

import DropDown from "./Dropdown.vue";
import PaperTable from "./PaperTable.vue";
import Button from "./Button";

import Card from "./Cards/Card.vue";
import ChartCard from "./Cards/ChartCard.vue";
import StatsCard from "./Cards/StatsCard.vue";

import SidebarPlugin from "./SidebarPlugin/index";

let components = {
  FormGroupInput,
  Card,
  ChartCard,
  StatsCard,
  PaperTable,
  DropDown,
  SidebarPlugin,
};

export default components;

export {
  FormGroupInput,
  Card,
  ChartCard,
  StatsCard,
  PaperTable,
  DropDown,
  Button,
  SidebarPlugin,
};
