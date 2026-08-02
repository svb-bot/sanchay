const paymentModeSchema = {
    title: "Payment Mode",
    endpoint: "/payment-mode",

    fields: [
        {
            name: "mode_name",
            label: "Mode Name",
            type: "text",
            required: true
        }
    ]
};

export default paymentModeSchema;