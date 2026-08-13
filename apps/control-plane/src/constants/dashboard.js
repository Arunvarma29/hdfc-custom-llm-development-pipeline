import {
  FaDatabase,
  FaCloudUploadAlt,
  FaClock,
  FaCheckCircle,
} from "react-icons/fa";

import {
  BsCloudUpload,
} from "react-icons/bs";

import {
  RiFileList3Line,
} from "react-icons/ri";

import {
  MdAssessment,
} from "react-icons/md";

import {
  FaBrain,
} from "react-icons/fa";

export const dashboardStats = [
  {
    title: "Total Datasets",
    value: 42,
    icon: FaDatabase,
  },
  {
    title: "Uploaded Today",
    value: 5,
    icon: FaCloudUploadAlt,
  },
  {
    title: "Pending Review",
    value: 3,
    icon: FaClock,
  },
  {
    title: "Approved",
    value: 34,
    icon: FaCheckCircle,
  },
];

export const quickActions = [
  {
    title: "Upload Dataset",
    icon: BsCloudUpload,
    route: "/datasets",
    enabled: true,
  },
  {
    title: "Prepare Dataset",
    icon: RiFileList3Line,
    route: "/data-preparation",
    enabled: false,
  },
  {
    title: "Start Training",
    icon: FaBrain,
    route: "/fine-tuning",
    enabled: false,
  },
  {
    title: "Evaluate Model",
    icon: MdAssessment,
    route: "/evaluation",
    enabled: false,
  },
];

export const recentDatasets = [
  {
    name: "Banking FAQ",
    type: "FAQ",
    status: "Uploaded",
  },
  {
    name: "Customer Complaints",
    type: "Complaints",
    status: "Uploaded",
  },
  {
    name: "UPI Transactions",
    type: "Transactions",
    status: "Pending",
  },
];