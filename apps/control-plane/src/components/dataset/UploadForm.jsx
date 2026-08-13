"use client";

import { useState } from "react";
import { useCreateDataset } from "@/hooks/useCreateDataset";
import { DATASET_TYPES, DOMAINS } from "@/constants/datasetOptions";

export default function UploadForm({ onClose }) {
  const [form, setForm] = useState({
    name: "",
    description: "",
    dataset_type: "",
    domain: "",
    version: "1.0.0",
    file: null,
  });

  const { mutate, isPending } = useCreateDataset();

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleFileChange = (e) => {
    setForm((prev) => ({
      ...prev,
      file: e.target.files[0],
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData();

    formData.append("name", form.name);
    formData.append("description", form.description);
    formData.append("dataset_type", form.dataset_type);
    formData.append("domain", form.domain);
    formData.append("version", form.version);
    formData.append("file", form.file);

    mutate(formData, {
      onSuccess: () => {
        onClose();
      },
    });
  };
  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div className="space-y-4 ">
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Dataset Name"
          className="w-full rounded-lg border p-3"
        />

        <textarea
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Description"
          className="w-full rounded-lg border p-3"
        />

        <select
          name="dataset_type"
          value={form.dataset_type}
          onChange={handleChange}
          className="w-full rounded-lg border p-3"
        >
          <option value="">Select Dataset Type</option>

          {DATASET_TYPES.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>

        <select
          name="domain"
          value={form.domain}
          onChange={handleChange}
          className="w-full rounded-lg border p-3"
        >
          <option value="">Select Domain</option>

          {DOMAINS.map((domain) => (
            <option key={domain} value={domain}>
              {domain}
            </option>
          ))}
        </select>

        <input
          name="version"
          value={form.version}
          onChange={handleChange}
          placeholder="Dataset Version"
          className="w-full rounded-lg border p-3"
        />

        <input
          type="file"
          placeholder="Upload file"
          onChange={handleFileChange}
          className="w-[15em] rounded-lg border p-2 bg-green-700 text-white input"
        />
       
      </div>
      <button
        type="submit"
        className="rounded-lg bg-blue-600 px-5 py-3 text-white hover:bg-blue-700"
        disabled={isPending}
      >
        {isPending ? "Uploading..." : "Upload Dataset"}
      </button>
    </form>
  );
}
