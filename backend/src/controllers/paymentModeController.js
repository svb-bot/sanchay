import { createPaymentMode, getAllPaymentModes, getPaymentModeById, updatePaymentMode, deletePaymentMode } from "../models/paymentModeModel.js";

export async function addPaymentMode(req, res) {
    try {
        const result = await createPaymentMode(req.body);

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

export async function fetchPaymentModes(req, res) {
    try {
        const rows = await getAllPaymentModes();

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

export async function fetchPaymentModeById(req, res) {
    try {
        const rows = await getPaymentModeById(req.params.id);

        if (rows.length === 0) {
            return res.status(404).json({
                success: false,
                message: "Payment mode not found"
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

export async function editPaymentMode(req, res) {
    try {
        const result = await updatePaymentMode(req.params.id, req.body);

        if (result.affectedRows === 0) {
            return res.status(404).json({
                success: false,
                message: "Payment mode not found"
            });
        }

        res.json({
            success: true,
            message: "Payment mode updated successfully"
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function removePaymentMode(req, res) {
    try {
        const result = await deletePaymentMode(req.params.id);

        if (result.affectedRows === 0) {
            return res.status(404).json({
                success: false,
                message: "Payment mode not found"
            });
        }

        res.json({
            success: true,
            message: "Payment mode deleted successfully"
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}