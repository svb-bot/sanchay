import db from "../config/db.js";

export async function createSpending(data) {
    const sql = `
        INSERT INTO fact_spending (
            bill_date,
            bill_category_id,
            bill_issuer_name,
            bill_amount,
            bill_reference,
            bill_payment_mode_id,
            bill_notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `;

    const [result] = await db.execute(sql, [
        data.bill_date,
        data.bill_category_id,
        data.bill_issuer_name,
        data.bill_amount,
        data.bill_reference,
        data.bill_payment_mode_id,
        data.bill_notes
    ]);

    return result;
}

export async function getAllSpending() {
    const [rows] = await db.execute(`
        SELECT *
        FROM fact_spending
        ORDER BY bill_date DESC, payment_id DESC
    `);

    return rows;
}

export async function getSpendingSummary(data) {
    const [rows] = await db.execute(`
    WITH main AS (
        SELECT dbc.category_name category
            ,sum(fs.bill_amount) AS total_amount
        FROM fact_spending fs
        INNER JOIN dim_bill_category dbc ON fs.bill_category_id = dbc.category_id
        GROUP BY 1
    ),
    split_1 AS (
        SELECT CONCAT (SUBSTRING_INDEX(category, '/', 1)) category
            ,total_amount
        FROM main
        WHERE category LIKE '%/%'
    ),
    split_2 AS (
        SELECT CONCAT (
                SUBSTRING_INDEX(category, '/', 1)
                ,'/'
                ,SUBSTRING_INDEX(SUBSTRING_INDEX(category, '/', 2), '/', - 1)
                ) category
            ,total_amount
        FROM main
        WHERE category LIKE '%/%/%'
    )
    SELECT *
    FROM (
        SELECT category
            ,total_amount
        FROM main
        
        UNION ALL
        
        SELECT category
            ,sum(total_amount) total_amount
        FROM split_1
        GROUP BY 1
        
        UNION ALL
        
        SELECT category
            ,sum(total_amount) total_amount
        FROM split_2
        GROUP BY 1
    ) a
    ORDER BY 1

    `);
    return rows;
}