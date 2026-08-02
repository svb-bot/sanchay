const billCategorySchema = {
    title: "Bill Category",

    endpoint: "/bill-category",

    fields: [
        {
            name: "category_name",
            label: "Category Name",
            type: "text",
            required: true
        }
    ]
}

export default billCategorySchema