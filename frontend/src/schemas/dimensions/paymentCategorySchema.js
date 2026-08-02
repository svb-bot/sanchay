const paymentCategorySchema = {
    title: "Payment Category",
    endpoint: "/payment-category",

    fields: [
        {
            name: "category_name",
            label: "Category Name",
            type: "text",
            required: true
        }
    ]
};

export default paymentCategorySchema;