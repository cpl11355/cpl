from pathlib import Path
notes = {
 'report-ny-kitchenware-summary.html': ('高SKU耗材的库存/配送/分层定价模型，可复用于IVD耗材与诊所供应链初筛', 'SKU-heavy consumables model reusable for IVD / clinic supply-chain screening'),
 'report-beauty-salon-summary.html': ('线下门店成本结构+获客复购模型，可复用于诊所/健康服务项目测算', 'Store cost and retention model reusable for clinic / health-service sizing'),
 'report-food-import-summary.html': ('进口依赖+合规+冷链/时效风险框架，可复用于原料药辅料供应链初筛', 'Import-compliance-cold-chain framework reusable for API screening'),
 'report-h-wholesale-case-summary.html': ('企业级诊断+可行性+路线图写法，医药早期项目过会材料直接复用此结构', 'Diagnostics-feasibility-roadmap reusable for pharma approval packs'),
 'report-r-capital-case-summary.html': ('资本+治理+合规三维评估，最接近医药早期项目投不投的判断逻辑', 'Capital-governance-compliance lens closest to early-pharma Go/No-Go'),
}
for fn, pair in notes.items():
    cn, en = pair
    p = Path(fn)
    t = p.read_text(encoding='utf-8')
    box = (
        '<div class="transfer-box" style="margin:26px 0;padding:16px 18px;'
        'border:1px solid #bfe9f5;background:#f2fdff;border-radius:14px;'
        'font-size:14px;line-height:1.7">'
        '<b>Transfer to pharma:</b><br>'
        '<span class="t-cn">' + cn + '。本报告为非医药领域方法实证，'
        '医药方向当前只接 Phase 0 桌面评估，详见'
        '<a href="index.html#future" style="text-decoration:underline">医药早期评估</a>。</span>'
        '<span class="t-en en">' + en + '.</span></div>'
    )
    if 'transfer-box' not in t:
        t = t.replace('<div class="cta-row">', box + '<div class="cta-row">')
    t = t.replace('返回研究案例', '返回方法实证')
    t = t.replace('Back to cases', 'Back to proof')
    p.write_text(t, encoding='utf-8')
print('ALL DONE')
