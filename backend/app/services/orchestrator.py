from app.agents.navigator_agent import (
    scan_repository_structure
)

from app.agents.analyst_agent import (
    analyze_security_issue
)

from app.agents.remediation_agent import (
    suggest_remediation
)

from app.agents.report_agent import (
    generate_report
)


def run_security_pipeline(
    repo_path,
    findings
):

    navigation_data = (
        scan_repository_structure(
            repo_path
        )
    )

    enriched_results = []

    for finding in findings:

        analysis = analyze_security_issue(
            finding,
            navigation_data
        )

        remediation = (
            suggest_remediation(
                finding
            )
        )

        enriched_results.append({
            \"finding\": finding,
            \"analysis\": analysis,
            \"remediation\": remediation
        })

    report = generate_report(
        enriched_results
    )

    return {
        \"results\": enriched_results,
        \"report\": report
    }