from prometheus_client import Counter, Gauge

ticket_created_total = Counter(
    "ticket_created_total",
    "Total tickets created",
    ["classification", "priority"]
)

ticket_total_gauge = Gauge(
    "ticket_total_gauge",
    "Current number of tickets (gauge)"
)
