export function formatFileSize(bytes) {
  if (!bytes) return "-";

  const units = ["Bytes", "KB", "MB", "GB"];

  let size = bytes;
  let unitIndex = 0;

  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }

  return `${size.toFixed(2)} ${units[unitIndex]}`;
}