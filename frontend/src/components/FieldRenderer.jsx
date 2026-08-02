import { useEffect, useState } from "react";

import {
    TextInput,
    NumberInput,
    Textarea,
    Select
} from "@mantine/core";

import { DateInput } from "@mantine/dates";

import api from "../api/api";


function FieldRenderer({ field, value, onChange }) {

    const [options, setOptions] = useState([]);

    useEffect(() => {

        if (field.dataSource) {
            loadOptions();

        } else if (field.data) {
            setOptions(
                field.data.map(item => ({
                    value: item,
                    label: item
                }))
            );
        }

    }, [field]);


    const loadOptions = async () => {
        try {

            const response = await api.get(field.dataSource);

            setOptions(
                response.data.data.map(item => ({
                    value: String(item.id),
                    label: item.name
                }))
            );

        } catch (error) {
            console.error(
                `Failed loading ${field.name}`,
                error
            );
        }
    };


    switch (field.type) {

        case "text":
            return (
                <TextInput
                    label={field.label}
                    required={field.required}
                    value={value || ""}
                    onChange={(e) =>
                        onChange(
                            field.name,
                            e.currentTarget.value
                        )
                    }
                />
            );


        case "currency":
        case "number":
            return (
                <NumberInput
                    label={field.label}
                    required={field.required}
                    value={value}
                    min={field.min}
                    decimalScale={2}
                    thousandSeparator=","
                    onChange={(val) =>
                        onChange(
                            field.name,
                            val
                        )
                    }
                />
            );


        case "textarea":
            return (
                <Textarea
                    label={field.label}
                    value={value || ""}
                    onChange={(e) =>
                        onChange(
                            field.name,
                            e.currentTarget.value
                        )
                    }
                />
            );


        case "date":
            return (
                <DateInput
                    label={field.label}
                    required={field.required}
                    value={value}
                    onChange={(val) =>
                        onChange(
                            field.name,
                            val
                        )
                    }
                />
            );


        case "select":
            return (
                <Select
                    label={field.label}
                    required={field.required}
                    data={options}
                    value={value}
                    onChange={(val) =>
                        onChange(
                            field.name,
                            val
                        )
                    }
                />
            );


        default:
            return null;
    }
}

export default FieldRenderer;