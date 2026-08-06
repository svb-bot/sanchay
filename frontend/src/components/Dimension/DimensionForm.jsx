import { Card, Title } from "@mantine/core"

import DynamicForm from "../DynamicForm"
import api from "../../api/api"

function DimensionForm({ schema, onSaved }) {
    const handleSubmit = async ({ data, onsuccess, onerror }) => {
        try {
            const response = await api.post(schema.endpoint, data)
            if (!response.data.success) {
                throw new Error(response.data.message || "Failed to save data.")
            }
            onsuccess(response.data.message || "Record saved successfully.")
            onSaved?.()
        } catch (error) {
            onerror(error || "An error occurred while saving data.")
        }
    }

    return (
        <Card withBorder>
            <Title order={4}>{schema.title}</Title>

            <DynamicForm schema={schema.fields} onSubmit={handleSubmit} />
        </Card>
    )
}

export default DimensionForm
