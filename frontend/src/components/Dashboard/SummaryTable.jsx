import { useEffect, useState } from "react"

import { Card, Table, Title, Loader, Center, Text } from "@mantine/core"
import { BarsList } from "@mantine/charts"
import { useMantineTheme } from "@mantine/core"

import api from "../../api/api"

function SummaryTable({ title, endpoint }) {
    const [loading, setLoading] = useState(true)
    const [rows, setRows] = useState([])

    const loadData = async () => {
        try {
            setLoading(true)

            const response = await api.get(endpoint)

            setRows(response.data.data)
        } catch (error) {
            console.error(error)
        } finally {
            setLoading(false)
        }
    }

    function addTabsBySlashCount(category) {
        const count = (category.match(/\//g) || []).length // number of '/'
        return "".repeat(count) + category
    }

    useEffect(() => {
        loadData()
    }, [])

    if (loading) {
        return (
            <Card withBorder>
                <Center py="xl">
                    <Loader />
                </Center>
            </Card>
        )
    }

    const chartData = rows
        .filter((row) => row.total_amount > 0 && row.category && !row.category.includes("/"))
        .sort((a, b) => b.total_amount - a.total_amount)
        .map((row, idx) => ({
            name: row.category,
            value: row.total_amount
        }))

    return (
        <Card withBorder shadow="sm">
            <Title order={4} mb="md">
                {title}
            </Title>

            <Center>
                <BarsList barColor="teal" data={chartData} />
            </Center>

            <Table striped highlightOnHover>
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th>Category</Table.Th>

                        <Table.Th ta="right">Amount</Table.Th>
                    </Table.Tr>
                </Table.Thead>

                <Table.Tbody>
                    {rows.map((row) => (
                        <Table.Tr key={row.category}>
                            <Table.Td>
                                <Text size="sm" style={{ paddingLeft: (row.category.match(/\//g) || []).length * 10 }}>
                                    {row.category || "Total"}
                                </Text>
                            </Table.Td>

                            <Table.Td ta="right">
                                ₹ {Number(row.total_amount).toLocaleString("en-IN", { minimumFractionDigits: 2 })}
                            </Table.Td>
                        </Table.Tr>
                    ))}
                </Table.Tbody>
            </Table>
        </Card>
    )
}

export default SummaryTable
