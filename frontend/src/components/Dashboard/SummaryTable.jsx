import { useEffect, useState } from "react";

import {
    Card,
    Table,
    Title,
    Loader,
    Center
} from "@mantine/core";

import api from "../../api/api";

function SummaryTable({ title, endpoint }) {

    const [loading, setLoading] = useState(true);
    const [rows, setRows] = useState([]);


    const loadData = async () => {

        try {

            setLoading(true);

            const response = await api.get(endpoint);

            setRows(response.data.data);

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }

    };


    useEffect(() => {
        loadData();
    }, []);


    if (loading) {
        return (
            <Card withBorder>
                <Center py="xl">
                    <Loader />
                </Center>
            </Card>
        );
    }


    return (

        <Card withBorder shadow="sm">

            <Title order={4} mb="md">
                {title}
            </Title>

            <Table striped highlightOnHover>

                <Table.Thead>

                    <Table.Tr>

                        <Table.Th>
                            Category
                        </Table.Th>

                        <Table.Th ta="right">
                            Total Amount
                        </Table.Th>

                    </Table.Tr>

                </Table.Thead>


                <Table.Tbody>

                    {
                        rows.map((row) => (

                            <Table.Tr key={row.category}>

                                <Table.Td>
                                    {row.category}
                                </Table.Td>

                                <Table.Td ta="right">
                                    ₹ {Number(row.total_amount).toLocaleString("en-IN")}
                                </Table.Td>

                            </Table.Tr>

                        ))
                    }

                </Table.Tbody>

            </Table>

        </Card>

    );

}

export default SummaryTable;