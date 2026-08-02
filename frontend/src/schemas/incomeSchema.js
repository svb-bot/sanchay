const incomeSchema = [
    {
        name: "payment_date",
        label: "Payment Date",
        type: "date",
        required: true
    },
    {
        name: "payment_category_id",
        label: "Category",
        type: "select",
        required: true,
        dataSource: "/payment-category"
    },
    {
        name: "payment_payee_name",
        label: "Received From",
        type: "text"
    },
    {
        name: "payment_amt",
        label: "Amount",
        type: "currency",
        required: true,
        min: 0
    },
    {
        name: "payment_mode_id",
        label: "Payment Mode",
        type: "select",
        dataSource: "/payment-mode"
    },
    {
        name: "payment_notes",
        label: "Notes",
        type: "textarea"
    }
]

export default incomeSchema