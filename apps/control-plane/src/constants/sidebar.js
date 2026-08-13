import {
  MdDashboard,
  MdAssessment,
  MdMonitorHeart,
  MdSettings,
} from "react-icons/md";

import {
  FaDatabase,
  FaBrain,
  FaBoxes,
  FaRocket,
} from "react-icons/fa";

import { RiFileList3Line } from "react-icons/ri";

export const sidebarItems = [
  {
    title: "Overview",
    href: "/overview",
    icon: MdDashboard,
  },
  {
    title: "Dataset Registry",
    href: "/datasets",
    icon: FaDatabase,
  },
  {
    title: "Data Preparation",
    href: "/data-preparation",
    icon: RiFileList3Line,
  },
  {
    title: "Fine Tuning",
    href: "/fine-tuning",
    icon: FaBrain,
  },
  {
    title: "Evaluation",
    href: "/evaluation",
    icon: MdAssessment,
  },
  {
    title: "Model Registry",
    href: "/model-registry",
    icon: FaBoxes,
  },
  {
    title: "Deployment",
    href: "/deployment",
    icon: FaRocket,
  },
  {
    title: "Monitoring",
    href: "/monitoring",
    icon: MdMonitorHeart,
  },
  {
    title: "Settings",
    href: "/settings",
    icon: MdSettings,
  },
];