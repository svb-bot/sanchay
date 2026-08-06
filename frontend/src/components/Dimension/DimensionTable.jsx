import { Table, ActionIcon, Group, Button, Card } from "@mantine/core"

import { IconTrash, IconRefresh, IconEdit } from "@tabler/icons-react"
import { forwardRef, useEffect, useImperativeHandle, useState } from "react"

import EditDimensionModal from "./EditDimensionModal"
import api from "../../api/api"

const DimensionTable = forwardRef(({ schema }, ref) => {
    const [rows, setRows] = useState([])
    const [opened, setOpened] = useState(false)
    const [selectedRecord, setSelectedRecord] = useState(null)

    const editRow = (record) => {
        setSelectedRecord(record)
        setOpened(true)
    }

    const loadData = async () => {
        try {
            const response = await api.get(schema.endpoint)

            setRows(response.data.data)
        } catch (error) {
            console.error(error)
        }
    }

    const deleteRow = async (id) => {
        await api.delete(`${schema.endpoint}/${id}`)

        loadData()
    }

    useEffect(() => {
        loadData()
    }, [schema.endpoint])

    return (
        <Card withBorder>
            <Group justify="space-between" mb="md">
                <Button leftSection={<IconRefresh size={16} />} variant="light" onClick={loadData}>
                    Refresh
                </Button>
            </Group>

            <Table striped highlightOnHover>
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th>ID</Table.Th>
                        <Table.Th>Name</Table.Th>
                        <Table.Th width={120}>Action</Table.Th>
                    </Table.Tr>
                </Table.Thead>

                <Table.Tbody>
                    {rows.map((row) => (
                        <Table.Tr key={row.id}>
                            <Table.Td>{row.id}</Table.Td>

                            <Table.Td>{row.name}</Table.Td>

                            <Table.Td>
                                <Group spacing="xs" mb="md">
                                    <ActionIcon color="blue" variant="light" onClick={() => editRow(row)}>
                                        <IconEdit size={16} />
                                    </ActionIcon>
                                    <ActionIcon color="red" onClick={() => deleteRow(row[schema.idField])}>
                                        <IconTrash size={16} />
                                    </ActionIcon>
                                </Group>
                            </Table.Td>
                        </Table.Tr>
                    ))}
                </Table.Tbody>
            </Table>

            <EditDimensionModal
                opened={opened}
                onClose={() => setOpened(false)}
                schema={schema}
                record={selectedRecord}
                onUpdated={loadData}
            />
        </Card>
    )
})

export default DimensionTable
