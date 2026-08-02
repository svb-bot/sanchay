import { createBillPaymentMode, getAllBillPaymentModes, getBillPaymentModeById, updateBillPaymentMode, deleteBillPaymentMode } from "../models/billPaymentModeModel.js";

export async function addBillPaymentMode(req, res) {
    try {
        const result = await createBillPaymentMode(req.body);

        res.status(201).json({
            success: true,
            mode_id: result.insertId
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function fetchBillPaymentModes(req, res) {
    try {
        const rows = await getAllBillPaymentModes();

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

export async function fetchBillPaymentModeById(req, res) {
    try {
        const rows = await getBillPaymentModeById(req.params.id);

        if (rows.length === 0) {
            return res.status(404).json({
                success: false,
                message: "Bill payment mode not found"
            });
        }

        res.json({
            success: true,
            data: rows[0]
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function editBillPaymentMode(req, res) {
    try {
        const result = await updateBillPaymentMode(req.params.id, req.body);

        if (result.affectedRows === 0) {
            return res.status(404).json({
                success: false,
                message: "Bill payment mode not found"
            });
        }

        res.json({
            success: true,
            message: "Bill payment mode updated successfully"
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function removeBillPaymentMode(req, res) {
    try {
        const result = await deleteBillPaymentMode(req.params.id);

        if (result.affectedRows === 0) {
            return res.status(404).json({
                success: false,
                message: "Bill payment mode not found"
            });
        }

        res.json({
            success: true,
            message: "Bill payment mode deleted successfully"
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}