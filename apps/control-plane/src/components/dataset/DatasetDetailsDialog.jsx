"use client";

import { useEffect, useState } from "react";

import Modal from "@/components/common/Modal";
import StatusBadge from "./StatusBadge";
import { formatFileSize } from "@/utils/formatFileSize";

import usePrepareDataset from "@/hooks/usePrepareDataset";
import usePreparationStatus from "@/hooks/usePreparationStatus";
import useApproveDataset from "@/hooks/useApproveDataset";
import useRejectDataset from "@/hooks/useRejectDataset";

import { useQueryClient } from "@tanstack/react-query";
import { QUERY_KEYS } from "@/constants/queryKeys";

export default function DatasetDetailsDialog({
  dataset,
  isOpen,
  onClose,
}) {
  const [preparation, setPreparation] = useState(null);
  const [reviewerName, setReviewerName] = useState("");
  const [reviewComment, setReviewComment] = useState("");
  const [reviewError, setReviewError] = useState("");
  const [reviewMessage, setReviewMessage] = useState("");

  const queryClient = useQueryClient();

  const refreshDatasets = async () => {
    await queryClient.invalidateQueries({
      queryKey: QUERY_KEYS.DATASETS,
    });
  };

  const { prepare, loading: preparing } = usePrepareDataset();
  const {
    getStatus,
    loading: checkingPreparation,
  } = usePreparationStatus();
  const { approve, loading: approving } =
    useApproveDataset();
  const { reject, loading: rejecting } =
    useRejectDataset();

  useEffect(() => {
    if (!dataset) {
      setReviewerName("");
      setReviewComment("");
      setReviewError("");
      setReviewMessage("");
      setPreparation(null);
      return;
    }

    setReviewerName(dataset.reviewer_name || "");
    setReviewComment(dataset.review_comment || "");
    setReviewError("");
    setReviewMessage("");
  }, [dataset]);

  if (!dataset) return null;

  const handlePrepare = async () => {
    try {
      const result = await prepare(dataset.id);
      setPreparation(result);
      await refreshDatasets();
    } catch {
      // Hook handles API error.
    }
  };



  const handleCheckPreparation = async () => {
    try {
      const result = await getStatus(dataset.id);
      setPreparation(result);
      await refreshDatasets();
    } catch {
      // Hook handles API error.
    }
  };




  const validateReview = (decision) => {
    const name = reviewerName.trim();
    const comment = reviewComment.trim();

    if (!name || name.length < 2) {
      setReviewError(
        "Reviewer name must contain at least 2 characters."
      );
      return null;
    }

    if (decision === "REJECT" && !comment) {
      setReviewError(
        "Please provide a reason before rejecting the dataset."
      );
      return null;
    }

    return {
      reviewer_name: name,
      comment: comment || null,
    };
  };

  const handleApprove = async () => {
    setReviewError("");
    setReviewMessage("");

    const review = validateReview("APPROVE");
    if (!review) return;

    try {
      await approve(dataset.id, review);
      setPreparation(null);
      setReviewMessage(
        "Dataset approved and its version has been frozen."
      );
      await refreshDatasets();
    } catch {
      // Hook handles API error.
    }
  };

  const handleReject = async () => {
    setReviewError("");
    setReviewMessage("");

    const review = validateReview("REJECT");
    if (!review) return;

    try {
      await reject(dataset.id, review);
      setPreparation(null);
      setReviewMessage(
        "Dataset rejected. Review details have been recorded."
      );
      await refreshDatasets();
    } catch {
      // Hook handles API error.
    }
  };


  const renderActions = () => {
    if (dataset.is_frozen) {
      return (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3">
          <p className="text-sm font-semibold text-emerald-800">
            Dataset is frozen
          </p>
          <p className="mt-1 text-xs text-emerald-700">
            This approved version cannot be modified,
            prepared again, or deleted.
          </p>
        </div>
      );
    }

    switch (dataset.status) {
      case "UPLOADED":
        return (
          <button
            onClick={handlePrepare}
            disabled={preparing}
            className="rounded-xl bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {preparing
              ? "Preparing..."
              : "Prepare Dataset"}
          </button>
        );

      case "PREPARING":
        return (
          <button
            onClick={handleCheckPreparation}
            disabled={checkingPreparation}
            className="rounded-xl bg-amber-500 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-amber-600 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {checkingPreparation
              ? "Checking..."
              : "Check Preparation"}
          </button>
        );

      case "READY":
        return (
          <div className="w-full rounded-2xl border border-blue-100 bg-blue-50 p-4">
            <div className="mb-4">
              <p className="text-sm font-semibold text-slate-900">
                Human / Data Owner Review
              </p>

              <p className="mt-1 text-xs text-slate-600">
                Review the prepared dataset before approving this version
                for model development.
              </p>
            </div>

            <div className="grid gap-3">
              <div>
                <label
                  htmlFor="reviewer-name"
                  className="mb-1.5 block text-xs font-semibold text-slate-600"
                >
                  Reviewer Name
                </label>

                <input
                  id="reviewer-name"
                  type="text"
                  value={reviewerName}
                  onChange={(event) => {
                    setReviewerName(event.target.value);
                    setReviewError("");
                    setReviewMessage("");
                  }}
                  placeholder="Enter reviewer / data owner name"
                  className="w-full rounded-xl border border-slate-300 bg-white px-3.5 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              <div>
                <label
                  htmlFor="review-comment"
                  className="mb-1.5 block text-xs font-semibold text-slate-600"
                >
                  Review Comment
                </label>

                <textarea
                  id="review-comment"
                  value={reviewComment}
                  onChange={(event) => {
                    setReviewComment(event.target.value);
                    setReviewError("");
                    setReviewMessage("");
                  }}
                  placeholder="Add review notes..."
                  rows={4}
                  className="w-full resize-none rounded-xl border border-slate-300 bg-white px-3.5 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              {reviewError && (
                <div className="rounded-xl border border-red-200 bg-red-50 px-3 py-2.5 text-sm text-red-700">
                  {reviewError}
                </div>
              )}

              {reviewMessage && (
                <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2.5 text-sm text-emerald-700">
                  {reviewMessage}
                </div>
              )}

              <div className="flex flex-col-reverse gap-2 pt-1 sm:flex-row sm:justify-end">
                <button
                  onClick={handleReject}
                  disabled={rejecting || approving}
                  className="rounded-xl border border-red-200 bg-white px-4 py-2.5 text-sm font-semibold text-red-600 transition hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {rejecting ? "Rejecting..." : "Reject"}
                </button>

                <button
                  onClick={handleApprove}
                  disabled={approving || rejecting}
                  className="rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {approving ? "Approving..." : "Approve & Freeze"}
                </button>
              </div>
            </div>
          </div>
        );

      case "APPROVED":
        return (
          <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3">
            <p className="text-sm font-semibold text-emerald-800">
              Dataset approved and frozen
            </p>

            {dataset.reviewer_name && (
              <p className="mt-1 text-xs text-emerald-700">
                Reviewed by {dataset.reviewer_name}
              </p>
            )}

            {dataset.reviewed_at && (
              <p className="text-xs text-emerald-700">
                {new Date(
                  dataset.reviewed_at
                ).toLocaleString()}
              </p>
            )}
          </div>
        );

      case "REJECTED":
        return (
          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3">
            <p className="text-sm font-semibold text-red-800">
              Dataset rejected
            </p>

            {dataset.reviewer_name && (
              <p className="mt-1 text-xs text-red-700">
                Reviewed by {dataset.reviewer_name}
              </p>
            )}

            {dataset.review_comment && (
              <p className="mt-2 text-sm text-red-700">
                {dataset.review_comment}
              </p>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Dataset Details"
    >
      <div className="w-full max-w-3xl">
        <div className="max-h-[70vh] overflow-y-auto pr-2">
          <div className="space-y-5">
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-xl font-bold text-slate-900">
                    {dataset.name}
                  </h2>
                  <p className="mt-1 text-sm text-slate-500">
                    Version {dataset.version}
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <StatusBadge status={dataset.status} />

                  {dataset.is_frozen && (
                    <span className="inline-flex rounded-full bg-violet-50 px-3 py-1 text-xs font-semibold text-violet-700 ring-1 ring-inset ring-violet-200">
                      FROZEN
                    </span>
                  )}
                </div>
              </div>
            </div>

            <section>
              <SectionTitle title="Dataset Information" />

              <div className="grid gap-3 rounded-2xl border border-slate-200 bg-white p-4 sm:grid-cols-2">
                <Detail label="Dataset Type" value={dataset.dataset_type} />
                <Detail label="Banking Domain" value={dataset.domain} />
                <Detail label="Version" value={dataset.version} />
                <Detail label="File Name" value={dataset.file_name} />
                <Detail label="File Size" value={formatFileSize(dataset.file_size)} />
                <Detail label="Content Type" value={dataset.content_type} />
                <Detail
                  label="Created"
                  value={new Date(dataset.created_at).toLocaleString()}
                />
                <Detail
                  label="Updated"
                  value={new Date(dataset.updated_at).toLocaleString()}
                />

                <div className="sm:col-span-2">
                  <Detail label="Description" value={dataset.description} />
                </div>
              </div>
            </section>

            <section>
              <SectionTitle title="Preparation" />

              <div className="rounded-2xl border border-slate-200 bg-white p-4">
                {preparation ? (
                  <div className="grid gap-3 sm:grid-cols-2">
                    <Detail label="Job ID" value={preparation.id} />
                    <Detail label="Status" value={preparation.status} />
                    <Detail label="Attempts" value={preparation.attempts} />
                    <Detail
                      label="Started"
                      value={
                        preparation.started_at
                          ? new Date(preparation.started_at).toLocaleString()
                          : "—"
                      }
                    />
                    <Detail
                      label="Completed"
                      value={
                        preparation.completed_at
                          ? new Date(preparation.completed_at).toLocaleString()
                          : "—"
                      }
                    />

                    {preparation.error_message && (
                      <div className="sm:col-span-2">
                        <Detail label="Error" value={preparation.error_message} />
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-sm text-slate-500">
                    No preparation details loaded yet.
                  </p>
                )}
              </div>
            </section>

            <section>
              <SectionTitle title="Governance" />

              <div className="grid gap-3 rounded-2xl border border-slate-200 bg-white p-4 sm:grid-cols-2">
                <Detail label="Lifecycle Status" value={dataset.status} />
                <Detail
                  label="Frozen"
                  value={dataset.is_frozen ? "Yes" : "No"}
                />
                <Detail
                  label="Frozen At"
                  value={
                    dataset.frozen_at
                      ? new Date(dataset.frozen_at).toLocaleString()
                      : "—"
                  }
                />
                <Detail label="Dataset ID" value={dataset.id} />
                <Detail
                  label="Reviewer"
                  value={dataset.reviewer_name || "—"}
                />
                <Detail
                  label="Reviewed At"
                  value={
                    dataset.reviewed_at
                      ? new Date(
                          dataset.reviewed_at
                        ).toLocaleString()
                      : "—"
                  }
                />
                <div className="sm:col-span-2">
                  <Detail
                    label="Review Comment"
                    value={dataset.review_comment || "—"}
                  />
                </div>
              </div>
            </section>

            <section className="border-t border-slate-200 pt-5">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>{renderActions()}</div>

                <div className="flex gap-3">
                  <button
                    onClick={onClose}
                    className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                  >
                    Close
                  </button>

                  <a
                    href={`http://127.0.0.1:8001/api/v1/datasets/${dataset.id}/download`}
                    target="_blank"
                    rel="noreferrer"
                    className="rounded-xl bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800"
                  >
                    Open File
                  </a>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </Modal>
  );
}

function SectionTitle({ title }) {
  return (
    <h3 className="mb-3 text-sm font-bold uppercase tracking-wider text-slate-500">
      {title}
    </h3>
  );
}

function Detail({ label, value }) {
  return (
    <div className="rounded-xl bg-slate-50 p-3">
      <p className="text-xs font-medium text-slate-500">{label}</p>
      <p className="mt-1 break-all text-sm font-medium text-slate-900">
        {value ?? "—"}
      </p>
    </div>
  );
}