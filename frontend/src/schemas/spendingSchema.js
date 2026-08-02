const spendingSchema = [
    {
        name: "bill_date",
        label: "Bill Date",
        type: "date",
        required: true
    },
    {
        name: "bill_category_id",
        label: "Category",
        type: "select",
        required: true,
        dataSource: "/bill-category"
    },
    {
        name: "bill_issuer_name",
        label: "Merchant / Issuer",
        type: "text"
    },
    {
        name: "bill_amount",
        label: "Amount",
        type: "currency",
        required: true,
        min: 0
    },
    {
        name: "bill_reference",
        label: "Reference No.",
        type: "text"
    },
    {
        name: "bill_payment_mode_id",
        label: "Payment Mode",
        type: "select",
        dataSource: "/bill-payment-mode"
    },
    {
        name: "bill_notes",
        label: "Notes",
        type: "textarea"
    }
]

export default spendingSchema