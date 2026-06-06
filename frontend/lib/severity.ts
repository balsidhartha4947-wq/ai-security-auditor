export function getSeverityColor(severity: string) {
  switch (severity?.toUpperCase()) {
    case "ERROR":
    case "HIGH":
      return "bg-red-500"

    case "WARNING":
    case "MEDIUM":
      return "bg-yellow-500"

    case "INFO":
    case "LOW":
      return "bg-blue-500"

    default:
      return "bg-gray-500"
  }
}