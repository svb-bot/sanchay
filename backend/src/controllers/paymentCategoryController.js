import { getAllPaymentCategories, createPaymentCategory, updatePaymentCategory, deletePaymentCategory, getPaymentCategoryById } from "../models/paymentCategoryModel.js";

export async function fetchPaymentCategories(req, res) {
    try {
        const rows = await getAllPaymentCategories();

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

export async function addPaymentCategory(req, res) {
    try {
        const result = await createPaymentCategory(req.body);

        res.status(201).json({
            success: true,
            category_id: result.insertId
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function editPaymentCategory(req, res) {
    try {
        const { id } = req.params;
        const result = await updatePaymentCategory(id, req.body);

        if (result.affectedRows === 0) {
            return res.status(404).json({
                success: false,
                message: "Payment category not found"
            });
        }

        res.json({
            success: true,
            message: "Payment category updated successfully"
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function removePaymentCategory(req, res) {
    try {
        const { id } = req.params;
        const result = await deletePaymentCategory(id);

        if (result.affectedRows === 0) {
            return res.status(404).json({
                success: false,
                message: "Payment category not found"
            });
        }

        res.json({
            success: true,
            message: "Payment category deleted successfully"
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function fetchPaymentCategoryById(req, res) {
    try {
        const { id } = req.params;
        const category = await getPaymentCategoryById(id);

        if (!category) {
            return res.status(404).json({
                success: false,
                message: "Payment category not found"
            });
        }

        res.json({
            success: true,
            data: category
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}