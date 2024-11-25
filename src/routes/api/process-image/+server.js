import { json } from '@sveltejs/kit';

export const POST = async ({ request }) => {
    try {
        const { imagePath, timestamp } = await request.json(); // 修改 imageData 为 imagePath

        if (!imagePath || !timestamp) {
            return json({ error: '缺少必要参数' }, { status: 400 });
        }

        // 调用 Python 脚本处理图片
        const response = await fetch('http://localhost:5000/process-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ imagePath, timestamp }) // 修改 imageData 为 imagePath
        });

        if (!response.ok) {
            // 如果响应状态不是 2xx，抛出错误
            const errorBody = await response.json();
            throw new Error(errorBody.error || '调用 Python 脚本失败');
        }

        const result = await response.json();

        return json(result, { status: 200 });
    } catch (error) {
        console.error('处理图片出错:', error);
        return json({ error: '处理图片出错' }, { status: 500 });
    }
};