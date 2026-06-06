def generate_report(
    findings
):

    report = \"# Security Audit Report\\n\\n\"

    for item in findings:

        report += (
            f\"## {item['finding']}\\n\"
        )

        report += (
            f\"Severity: "
            f\"{item['severity']}\\n\\n\"
        )

        report += (
            f\"Analysis:\\n"
            f\"{item['analysis']}\\n\\n\"
        )

        report += (
            f\"Remediation:\\n"
            f\"{item['remediation']}\\n\\n\"
        )

    return report