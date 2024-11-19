import { json } from '@sveltejs/kit'
import { spawn } from 'child_process'
import fs from 'fs'
import path from 'path'

// 确保 saved 文件夹存在
const savedDir = path.join(process.cwd(), 'saved')
if (!fs.existsSync(savedDir)) {
    fs.mkdirSync(savedDir)
}

export async function POST({ request }) {
    const { imageData, timestamp } = await request.json()
    
    // 创建临时文件夹（如果不存在）
    const savedDir = path.join(process.cwd(), 'saved')
    if (!fs.existsSync(savedDir)) {
        fs.mkdirSync(savedDir)
    }
    
    // 保存base64图片数据为临时文件
    const imagePath = path.join(savedDir, `${timestamp}.png`)
    fs.writeFileSync(imagePath, Buffer.from(imageData, 'base64'))
    
    // 运行Python脚本
    const pythonProcess = spawn('python', ['scripts/process_image.py', imagePath])
    
    return new Promise((resolve) => {
        pythonProcess.on('close', (code) => {
            // 清理临时文件
            fs.unlinkSync(imagePath)
            
            if (code !== 0) {
                resolve(json({ error: '脚本执行失败' }, { status: 500 }))
            } else {
                resolve(json({ success: true, message: '脚本执行成功' }))
            }
        })
        
        pythonProcess.on('error', (err) => {
            // 清理临时文件
            if (fs.existsSync(imagePath)) {
                fs.unlinkSync(imagePath)
            }
            resolve(json({ error: err.message }, { status: 500 }))
        })
    })
} 