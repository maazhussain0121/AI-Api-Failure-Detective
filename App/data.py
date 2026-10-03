INCIDENTS = [
    {
        "id": "INC-001",
        "endpoint": "POST /api/orders",
        "status_code": 500,
        "service": "order-service",
        "timestamp": "2026-10-03T14:32:21",
        "duration_ms": 1240,
        "logs": [
            "14:32:18 INFO order creation started",
            "14:32:19 INFO calling payment-service",
            "14:32:20 INFO payment request started",
            "14:32:21 ERROR database connection timeout",
            "14:32:21 ERROR payment transaction failed",
            "14:32:21 ERROR order creation failed"
        ]
    },
    {
        "id": "INC-002",
        "endpoint": "POST /api/payment",
        "status_code": 504,
        "service": "payment-service",
        "timestamp": "2026-10-03T15:10:42",
        "duration_ms": 5200,
        "logs": [
            "15:10:35 INFO payment request received",
            "15:10:36 INFO contacting external payment provider",
            "15:10:41 ERROR payment provider timeout",
            "15:10:42 ERROR payment request failed",
            "15:10:42 ERROR returning HTTP 504"
        ]
    },
    {
        "id": "INC-003",
        "endpoint": "GET /api/users/profile",
        "status_code": 401,
        "service": "auth-service",
        "timestamp": "2026-10-03T16:02:11",
        "duration_ms": 85,
        "logs": [
            "16:02:10 INFO profile request received",
            "16:02:10 INFO validating authentication token",
            "16:02:11 ERROR JWT token expired",
            "16:02:11 ERROR authentication failed",
            "16:02:11 INFO returning HTTP 401"
        ]
    }
]