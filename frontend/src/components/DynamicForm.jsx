import { useEffect, useState } from "react"
import { Stack, Group, Button } from "@mantine/core"
import { notifications } from "@mantine/notifications"

import FieldRenderer from "./FieldRenderer"

function DynamicForm({ schema, initialValues = {}, onSubmit, submitLabel = "Save" }) {
    const [values, setValues] = useState(initialValues)

    // useEffect(() => {
    //     setValues(initialValues)
    // }, [initialValues])

    const handleChange = (name, value) => {
        setValues((prev) => ({
            ...prev,
            [name]: value
        }))
    }

    const clearForm = () => {
        setValues(initialValues)
    }

    const validate = () => {
        for (const field of schema) {
            if (
                field.required &&
                (values[field.name] === undefined || values[field.name] === null || values[field.name] === "")
            ) {
                return false
            }
        }

        return true
    }

    const transformData = () => {
        const data = { ...values }

        schema.forEach((field) => {
            if (field.type === "date" && data[field.name] instanceof Date) {
                data[field.name] = data[field.name].toISOString().split("T")[0]
            }
        })

        return data
    }

    const handleSubmit = () => {
        if (!validate()) {
            return
        }

        const data = transformData()

        onSubmit({
            data,
            onsuccess: (msg) => {
                clearForm()
                notifications.show({ title: "Success", message: msg })
                setValues(initialValues)
            },
            onerror: (msg) => notifications.show({ color: "red", title: "Oops", message: msg })
        })
        
    }

    return (
        <Stack>
            {schema.map((field) => (
                <FieldRenderer key={field.name} field={field} value={values[field.name]} onChange={handleChange} />
            ))}

            <Group justify="flex-end">
                <Button onClick={handleSubmit}>{submitLabel}</Button>
            </Group>
        </Stack>
    )
}

export default DynamicForm
