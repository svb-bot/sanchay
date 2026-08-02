import { Card } from "@mantine/core"

import DynamicForm from "../components/DynamicForm"
import spendingSchema from "../schemas/spendingSchema"
import api from "../api/api"

function SpendingForm() {
    const saveSpending = async ({ data, onsuccess, onerror }) => {
        try {
            const response = await api.post("/spending", data)
            if (!response.data.success) {
                throw new Error(response.data.message || "Failed to save data.")
            }
            onsuccess(response.data.message || "Data saved successfully.")
        } catch (error) {
            onerror(error || "An error occurred while saving data.")
        }
    }

    return (
        <Card withBorder shadow="sm">
            <DynamicForm schema={spendingSchema} onSubmit={saveSpending} submitLabel="Save Spending" />
        </Card>
    )
}

export default SpendingForm
