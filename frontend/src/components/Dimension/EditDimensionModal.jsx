import { Modal, Title } from "@mantine/core"
import { notifications } from "@mantine/notifications"

import api from "../../api/api"
import DynamicForm from "../DynamicForm"

function EditDimensionModal({ opened, onClose, schema, record, onUpdated }) {
    if (!record) {
        return null
    }

    const handleSubmit = async ({ data, onsuccess, onerror }) => {
        try {
            const response = await api.put(`${schema.endpoint}/${record.id}`, data)
            if (!response.data.success) {
                throw new Error(response.data.message || "Unable to update record.")
            }
            onsuccess(response.data.message || "Record updated successfully.")
            onUpdated?.()
            onClose()
        } catch (error) {
            onerror(error || "An error occurred while updating record.")
        }
    }

    return (
        <Modal opened={opened} onClose={onClose} title={<Title order={2}>Edit {schema.title}</Title>} centered>
            <DynamicForm schema={schema.fields} initialValues={record} submitLabel="Update" onSubmit={handleSubmit} />
        </Modal>
    )
}

export default EditDimensionModal
