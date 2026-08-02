import { Card } from "@mantine/core"
import { notifications } from "@mantine/notifications"

import DynamicForm from "../components/DynamicForm"
import incomeSchema from "../schemas/incomeSchema"
import api from "../api/api"

function IncomeForm() {
    const saveIncome = async ({ data, onsuccess, onerror }) => {
        try {
            const response = await api.post("/income", data)
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
            <DynamicForm schema={incomeSchema} onSubmit={saveIncome} />
        </Card>
    )
}

export default IncomeForm
