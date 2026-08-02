const billPaymentModeSchema = {
    title: "Bill Payment Mode",

    endpoint: "/bill-payment-mode",

    fields: [
        {
            name: "mode_name",
            label: "Mode Name",
            type: "text",
            required: true
        }
    ]
};

export default billPaymentModeSchema;