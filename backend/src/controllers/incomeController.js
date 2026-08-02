import { createIncome, getAllIncome } from "../models/incomeModel.js";

export async function addIncome(req, res) {
    try {
        const result = await createIncome(req.body);

        res.status(201).json({
            success: true,
            payment_id: result.insertId
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function fetchIncome(req, res) {
    try {
        const rows = await getAllIncome();

        res.json({
            success: true,
            data: rows
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}