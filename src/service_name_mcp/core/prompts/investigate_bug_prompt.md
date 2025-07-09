# Investigate {{Domain}} Issue - Investigation Guide

This guide will help you systematically investigate issue ID: **{{issue_id}}**

## Investigation Framework

### 1. **Issue Context Analysis**
- Review the original issue report and description
- Understand the business impact and urgency
- Identify affected systems, data sources, or processes
- Note the timeline when the issue was first observed

### 2. **Data Validation Steps**
- Verify data completeness for the affected time period
- Check for any recent data pipeline or system changes
- Compare current data patterns with historical baselines
- Validate data quality metrics and consistency checks

### 3. **Root Cause Analysis**
- Examine underlying data sources and transformations
- Review recent system changes, deployments, or updates
- Check for external factors (holidays, system maintenance, etc.)
- Analyze error patterns and frequency

### 4. **Impact Assessment**
- Quantify the scope of affected data or processes
- Identify downstream dependencies and systems
- Assess business impact and user experience effects
- Determine urgency and priority for resolution

### 5. **Solution Development**
- Identify potential fixes or workarounds
- Test proposed solutions with sample data
- Validate that fixes don't introduce new issues
- Document the solution approach and reasoning

## Investigation Tools and Queries

### Data Quality Checks
```kql
// Example: Check data completeness over time
TableName
| where TimeGenerated >= ago(7d)
| summarize RecordCount = count() by bin(TimeGenerated, 1h)
| render timechart
```

### Error Pattern Analysis
```kql
// Example: Analyze error patterns
LogTable
| where TimeGenerated >= ago(24h)
| where Level == "Error"
| summarize ErrorCount = count() by ErrorType, bin(TimeGenerated, 1h)
| render timechart
```

### Baseline Comparison
```kql
// Example: Compare metrics to baseline
MetricsTable
| where TimeGenerated >= ago(14d)
| summarize AvgMetric = avg(MetricValue) by bin(TimeGenerated, 1d)
| extend Baseline = avg(AvgMetric)
| extend Deviation = (AvgMetric - Baseline) / Baseline * 100
| render timechart
```

## Documentation and Communication

### Investigation Log
Maintain a detailed log of:
- Queries executed and results found
- Hypotheses tested and outcomes
- Data anomalies or patterns discovered
- External factors or changes identified

### Status Updates
Provide regular updates including:
- Current investigation status
- Key findings and evidence
- Next steps and timeline
- Any immediate workarounds available

### Resolution Documentation
Once resolved, document:
- Root cause analysis summary
- Solution implemented
- Validation steps taken
- Prevention measures for the future

## Escalation Criteria

Escalate the investigation if:
- Issue impacts critical business processes
- Root cause cannot be identified within reasonable time
- Solution requires system changes beyond your authority
- Multiple teams or systems are involved
- Data integrity concerns are identified

## Follow-up Actions

After resolution:
1. Verify the fix resolves the original issue
2. Monitor for any recurrence or new related issues
3. Update documentation with lessons learned
4. Consider preventive measures or monitoring improvements
5. Communicate resolution to all stakeholders

Ready to help you investigate this {{domain}} issue systematically and thoroughly!
