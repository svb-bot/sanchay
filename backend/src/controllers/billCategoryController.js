import { createBillCategory, getAllBillCategories, getBillCategoryById, updateBillCategory, deleteBillCategory } from "../models/billCategoryModel.js";

export async function addBillCategory(req, res) {
    try {
        const result = await createBillCategory(req.body);

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

export async function fetchBillCategories(req, res) {
    try {
        const rows = await getAllBillCategories();

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

export async function fetchBillCategoryById(req, res) {
    try {
        const rows = await getBillCategoryById(req.params.id);

        if (rows.length === 0) {
            return res.status(404).json({
                success: false,
                message: "Bill category not found"
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

export async function editBillCategory(req, res) {
    try {
        const result = await updateBillCategory(req.params.id, req.body);

        if (result.affectedRows === 0) {
            return res.status(404).json({
                success: false,
                message: "Bill category not found"
            });
        }

        res.json({
            success: true,
            message: "Bill category updated successfully"
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function removeBillCategory(req, res) {
    try {
        const result = await deleteBillCategory(req.params.id);

        if (result.affectedRows === 0) {
            return res.status(404).json({
                success: false,
                message: "Bill category not found"
            });
        }

        res.json({
            success: true,
            message: "Bill category deleted successfully"
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}