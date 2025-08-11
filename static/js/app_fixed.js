// 八字能量解读系统 - 修复版JavaScript
class BaziApp {
    constructor() {
        console.log('BaziApp 初始化开始');
        this.initializeElements();
        this.bindEvents();
        this.showInputSection();
        console.log('BaziApp 初始化完成');
    }

    initializeElements() {
        console.log('获取页面元素...');
        
        // 获取所有必需的元素
        this.form = document.getElementById('baziForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.loading = document.getElementById('loading');
        this.resultSection = document.getElementById('resultSection');
        this.resultContent = document.getElementById('resultContent');
        this.newAnalysisBtn = document.getElementById('newAnalysis');
        this.inputSection = document.querySelector('.input-section');
        
        // 表单输入元素
        this.nameInput = document.getElementById('name');
        this.genderInput = document.getElementById('gender');
        this.birthYearInput = document.getElementById('birth_year');
        this.birthMonthInput = document.getElementById('birth_month');
        this.birthDayInput = document.getElementById('birth_day');
        this.birthTimeInput = document.getElementById('birth_time');
        this.locationInput = document.getElementById('location');
        this.questionInput = document.getElementById('question');
        
        // 验证关键元素
        const requiredElements = {
            form: this.form,
            submitBtn: this.submitBtn,
            nameInput: this.nameInput
        };
        
        const missing = [];
        for (const [name, element] of Object.entries(requiredElements)) {
            if (!element) {
                missing.push(name);
            }
        }
        
        if (missing.length > 0) {
            console.error('缺失的页面元素:', missing);
        } else {
            console.log('所有关键元素获取成功');
        }
    }

    bindEvents() {
        console.log('绑定事件...');
        
        // 表单提交事件
        if (this.form && this.submitBtn) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
            
            // 同时绑定按钮点击事件作为备用
            this.submitBtn.addEventListener('click', (e) => {
                console.log('按钮点击事件触发');
                if (e.target.form) {
                    // 如果按钮在表单内，让表单处理提交
                    return;
                } else {
                    // 如果不在表单内，手动处理
                    e.preventDefault();
                    this.handleSubmit(e);
                }
            });
            
            console.log('表单和按钮事件绑定成功');
        }
        
        // 重新分析按钮
        if (this.newAnalysisBtn) {
            this.newAnalysisBtn.addEventListener('click', () => this.showInputSection());
        }
        
        console.log('所有事件绑定完成');
    }

    async handleSubmit(e) {
        e.preventDefault();
        console.log('处理表单提交');
        
        // 收集表单数据
        const formData = this.collectFormData();
        console.log('表单数据:', formData);
        
        // 简单验证
        if (!formData.name || !formData.gender || !formData.birth_year || 
            !formData.birth_month || !formData.birth_day || !formData.birth_time) {
            this.showError('请填写完整的基本信息');
            return;
        }
        
        // 提交数据
        this.showLoading();
        
        try {
            const result = await this.submitToAPI(formData);
            this.displayResult(result);
        } catch (error) {
            console.error('提交错误:', error);
            this.showError(error.message);
        }
    }
    
    collectFormData() {
        // 解析时间输入 (HH:MM 格式)
        const timeValue = this.birthTimeInput?.value || '12:00';
        const [hour, minute] = timeValue.split(':').map(num => parseInt(num));
        
        return {
            name: this.nameInput?.value?.trim() || '',
            gender: this.genderInput?.value || '',
            birth_year: parseInt(this.birthYearInput?.value) || 0,
            birth_month: parseInt(this.birthMonthInput?.value) || 0,
            birth_day: parseInt(this.birthDayInput?.value) || 0,
            birth_hour: hour || 0,
            birth_minute: minute || 0,
            birth_time: timeValue, // 保留原始时间字符串用于验证
            location: this.locationInput?.value?.trim() || '北京',
            question: this.questionInput?.value?.trim() || ''
        };
    }

    async submitToAPI(formData) {
        console.log('发送API请求');
        
        const response = await fetch('/interpret', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({detail: '网络请求失败'}));
            throw new Error(errorData.detail || '服务器错误');
        }

        const data = await response.json();
        if (!data.ok) {
            throw new Error('分析失败，请重试');
        }

        return data.result;
    }

    displayResult(result) {
        console.log('显示结果');
        this.hideLoading();
        this.showResultSection();
        
        let html = '';
        
        // 用户信息
        if (result['用户信息']) {
            html += this.renderUserInfo(result['用户信息']);
        }
        
        // 八字信息
        if (result['bazi']) {
            html += this.renderBaziInfo(result['bazi']);
        }
        
        // 大运信息 (新增)
        if (result['大运信息']) {
            html += this.renderDayunInfo(result['大运信息']);
        }
        
        // 命局判定 (新增)
        if (result['命局判定']) {
            html += this.renderJujuDetection(result['命局判定']);
        }
        
        // 能量画像 (新增)
        if (result['能量画像']) {
            html += this.renderEnergyPortrait(result['能量画像']);
        }
        
        // 问题分析 (新增)
        if (result['问题分析']) {
            html += this.renderQuestionAnalysis(result['问题分析']);
        }
        
        // 五行生克关系可视化 (新增)
        if (result['五行生克关系']) {
            html += this.renderWuxingRelationshipChart(result['五行生克关系']);
        }
        
        // 启发引导 (新增)
        if (result['启发引导']) {
            html += this.renderInspirationGuide(result['启发引导']);
        }
        
        // 个性化方案 (新增)
        if (result['个性化方案']) {
            html += this.renderPersonalizedSolution(result['个性化方案']);
        }
        
        // 增强病药分析 (替换原有的病药分析)
        if (result['增强病药']) {
            html += this.renderEnhancedBingyao(result['增强病药']);
        } else if (result['定病药'] && result['定病药']['分级'] && result['定病药']['分级'][0]) {
            html += this.renderBingYaoAnalysis(result['定病药']['分级'][0]);
        }
        
        // 五行统计
        if (result['五行统计']) {
            html += this.renderElementsChart(result['五行统计']);
        }
        
        // 大白话说明 (新增)
        if (result['大白话说明']) {
            html += this.renderPlainLanguageSummary(result['大白话说明']);
        }
        
        this.resultContent.innerHTML = html || '<p>暂无结果数据</p>';
    }

    renderUserInfo(userInfo) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-user"></i> 用户信息</h3>
                <div class="content">
                    <p><strong>姓名：</strong>${userInfo['姓名']}</p>
                    <p><strong>性别：</strong>${userInfo['性别']}</p>
                    <p><strong>出生时间：</strong>${userInfo['出生时间']}</p>
                    <p><strong>出生地点：</strong>${userInfo['出生地点']}</p>
                </div>
            </div>
        `;
    }

    renderBaziInfo(baziInfo) {
        // 分离天干和地支
        const pillars = [baziInfo.year, baziInfo.month, baziInfo.day, baziInfo.hour];
        const tianGan = pillars.map(pillar => pillar.charAt(0)); // 天干
        const diZhi = pillars.map(pillar => pillar.charAt(1)); // 地支
        
        // 地支藏干映射表
        const zangGanMap = {
            '子': ['癸'],
            '丑': ['己', '癸', '辛'],
            '寅': ['甲', '丙', '戊'],
            '卯': ['乙'],
            '辰': ['戊', '乙', '癸'],
            '巳': ['丙', '庚', '戊'],
            '午': ['丁', '己'],
            '未': ['己', '丁', '乙'],
            '申': ['庚', '壬', '戊'],
            '酉': ['辛'],
            '戌': ['戊', '辛', '丁'],
            '亥': ['壬', '甲']
        };
        
        // 生成藏干显示
        const zangGanDisplay = diZhi.map(zhi => {
            const zangGan = zangGanMap[zhi] || [];
            if (zangGan.length > 1) {
                // 多个藏干：主气正常显示，其他作为下标
                return `${zangGan[0]}<sub>${zangGan.slice(1).join('')}</sub>`;
            }
            return zangGan[0] || '';
        });
        
        return `
            <div class="result-item">
                <h3><i class="fas fa-calendar-alt"></i> 八字信息</h3>
                <div class="bazi-display-new">
                    <div class="pillar-labels">
                        <span class="pillar-label">年柱</span>
                        <span class="pillar-label">月柱</span>
                        <span class="pillar-label">日柱</span>
                        <span class="pillar-label">时柱</span>
                    </div>
                    <div class="tiangan-row">
                        <span class="tiangan-cell">${tianGan[0]}</span>
                        <span class="tiangan-cell">${tianGan[1]}</span>
                        <span class="tiangan-cell">${tianGan[2]}</span>
                        <span class="tiangan-cell">${tianGan[3]}</span>
                    </div>
                    <div class="dizhi-row">
                        <span class="dizhi-cell">${diZhi[0]}<br><small class="zanggan">${zangGanDisplay[0]}</small></span>
                        <span class="dizhi-cell">${diZhi[1]}<br><small class="zanggan">${zangGanDisplay[1]}</small></span>
                        <span class="dizhi-cell">${diZhi[2]}<br><small class="zanggan">${zangGanDisplay[2]}</small></span>
                        <span class="dizhi-cell">${diZhi[3]}<br><small class="zanggan">${zangGanDisplay[3]}</small></span>
                    </div>
                </div>
            </div>
        `;
    }

    renderBingYaoAnalysis(bingyao) {
        return `
            <div class="result-item bingyao-analysis">
                <h3><i class="fas fa-pills"></i> 病药体系分析</h3>
                <div class="content">
                    <p><strong>命局类型：</strong>${bingyao['命局类型']}</p>
                    <p><strong>命局描述：</strong>${bingyao['命局描述']}</p>
                    <p><strong>能量本质：</strong>${bingyao['能量本质']}</p>
                    <p><strong>关系类型：</strong>${bingyao['关系类型']}</p>
                    
                    <div class="medicine-config">
                        <h4>病药配置</h4>
                        <div class="medicine-grid">
                            <div class="medicine-item chief">
                                <div class="medicine-label">君药</div>
                                <div class="medicine-name">${bingyao['病药配置']['君药']}</div>
                            </div>
                            <div class="medicine-item minister">
                                <div class="medicine-label">臣药</div>
                                <div class="medicine-name">${bingyao['病药配置']['臣药']}</div>
                            </div>
                            <div class="medicine-item assistant">
                                <div class="medicine-label">次药</div>
                                <div class="medicine-name">${bingyao['病药配置']['次药']}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="consciousness">
                        <h4>意识特质</h4>
                        <p>${bingyao['意识特质']}</p>
                    </div>
                </div>
            </div>
        `;
    }

    renderElementsChart(elements) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-chart-bar"></i> 五行统计</h3>
                <div class="content">
                    <p><strong>木：</strong>${elements.wood} <strong>火：</strong>${elements.fire} <strong>土：</strong>${elements.earth} <strong>金：</strong>${elements.metal} <strong>水：</strong>${elements.water}</p>
                    <p><strong>最旺：</strong>${elements['最旺']} <strong>最弱：</strong>${elements['最弱']}</p>
                </div>
            </div>
        `;
    }

    renderQuestion(question) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-question-circle"></i> 咨询问题</h3>
                <div class="content">
                    <p><strong>您的问题：</strong>${question}</p>
                    <p>基于您的八字分析和病药体系，系统为您提供了上述分析结果。</p>
                </div>
            </div>
        `;
    }

    showInputSection() {
        console.log('显示输入界面');
        if (this.inputSection) this.inputSection.style.display = 'block';
        if (this.resultSection) this.resultSection.style.display = 'none';
        if (this.loading) this.loading.style.display = 'none';
        
        // 重置表单
        if (this.form) this.form.reset();
    }

    showLoading() {
        console.log('显示加载状态');
        if (this.inputSection) this.inputSection.style.display = 'none';
        if (this.resultSection) this.resultSection.style.display = 'none';
        if (this.loading) this.loading.style.display = 'block';
    }

    hideLoading() {
        if (this.loading) this.loading.style.display = 'none';
    }

    showResultSection() {
        console.log('显示结果界面');
        if (this.inputSection) this.inputSection.style.display = 'none';
        if (this.resultSection) this.resultSection.style.display = 'block';
    }

    // 新增渲染函数
    renderDayunInfo(dayunInfo) {
        const currentDayun = dayunInfo['当前大运'] || {};
        const futureDayuns = dayunInfo['未来大运'] || [];
        const energyTimeline = dayunInfo['能量趋势图'] || null;
        
        // 渲染能量趋势图
        let energyTimelineHtml = '';
        if (energyTimeline) {
            energyTimelineHtml = this.renderEnergyTimeline(energyTimeline);
        }
        
        // 当前大运详情
        const currentDayunHtml = `
            <div class="current-dayun">
                <h4>🌟 当前大运 ${currentDayun.gan || ''}${currentDayun.zhi || ''}</h4>
                <div class="dayun-details">
                    <p><strong>年龄段：</strong>${currentDayun.age_range || '未知'}</p>
                    <p><strong>影响分析：</strong>${currentDayun.influence || '暂无分析'}</p>
                    ${currentDayun['人生阶段'] ? `<p><strong>人生阶段：</strong>${currentDayun['人生阶段']}</p>` : ''}
                    ${currentDayun['平衡分析'] ? `<p><strong>平衡分析：</strong>${currentDayun['平衡分析']}</p>` : ''}
                    ${currentDayun['平衡趋势'] ? `<p><strong>平衡趋势：</strong>${currentDayun['平衡趋势']}</p>` : ''}
                    ${currentDayun['关键机遇'] ? `<p><strong>🌈 关键机遇：</strong>${currentDayun['关键机遇']}</p>` : ''}
                    ${currentDayun['主要挑战'] ? `<p><strong>⚡ 主要挑战：</strong>${currentDayun['主要挑战']}</p>` : ''}
                    ${currentDayun['阶段建议'] ? `<p><strong>💡 阶段建议：</strong>${currentDayun['阶段建议']}</p>` : ''}
                </div>
            </div>
        `;
        
        // 未来大运展望
        let futureDayunHtml = '';
        if (futureDayuns.length > 0) {
            futureDayunHtml = `
                <div class="future-dayun">
                    <h4>🔮 未来大运展望</h4>
                    <div class="dayun-list">
                        ${futureDayuns.slice(0, 3).map(dayun => `
                            <div class="future-dayun-item">
                                <h5>${dayun.age_range} ${dayun.gan}${dayun.zhi}</h5>
                                <p><strong>影响：</strong>${dayun.influence}</p>
                                ${dayun['趋势展望'] ? `<p><strong>趋势：</strong>${dayun['趋势展望']}</p>` : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        return `
            <div class="result-item dayun-analysis">
                <h3><i class="fas fa-chart-line"></i> 大运分析</h3>
                <div class="content">
                    ${energyTimelineHtml}
                    ${currentDayunHtml}
                    ${futureDayunHtml}
                </div>
            </div>
        `;
    }
    
    renderEnergyTimeline(timelineData) {
        if (!timelineData || !timelineData.data_points) return '';
        
        const dataPoints = timelineData.data_points;
        const interactiveNodes = timelineData.interactive_nodes || [];
        
        // 创建SVG图表数据
        const maxAge = Math.max(...dataPoints.map(p => p.age));
        const minAge = Math.min(...dataPoints.map(p => p.age));
        const maxEnergy = Math.max(...dataPoints.map(p => p.energy));
        const minEnergy = Math.min(...dataPoints.map(p => p.energy));
        
        // 生成节点HTML
        const nodesHtml = interactiveNodes.map((node, index) => `
            <div class="energy-node" 
                 style="left: ${((node.age - minAge) / (maxAge - minAge)) * 100}%; 
                        bottom: ${((node.energy - minEnergy) / (maxEnergy - minEnergy)) * 80 + 10}%;"
                 data-node="${index}"
                 onclick="showDayunDetails(${index})">
                <div class="node-dot" style="background-color: ${node.color}"></div>
                <div class="node-label">${node.age}岁<br>${node.title}</div>
                <div class="node-tooltip" id="tooltip-${index}" style="display: none;">
                    <h6>${node.title}</h6>
                    <p><strong>能量指数:</strong> ${Math.round(node.energy)}</p>
                    ${node.opportunities ? `<p><strong>机遇:</strong> ${node.opportunities}</p>` : ''}
                    ${node.challenges ? `<p><strong>挑战:</strong> ${node.challenges}</p>` : ''}
                    ${node.balance_trend ? `<p><strong>趋势:</strong> ${node.balance_trend}</p>` : ''}
                    ${node.advice ? `<p><strong>建议:</strong> ${node.advice}</p>` : ''}
                    ${node.key_focus ? `<p><strong>重点:</strong> ${node.key_focus}</p>` : ''}
                </div>
            </div>
        `).join('');
        
        // 生成能量曲线路径
        const pathData = dataPoints.map((point, index) => {
            const x = ((point.age - minAge) / (maxAge - minAge)) * 100;
            const y = 90 - ((point.energy - minEnergy) / (maxEnergy - minEnergy)) * 80;
            return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
        }).join(' ');
        
        return `
            <div class="energy-timeline">
                <h4>📈 生命能量趋势图</h4>
                <div class="timeline-chart">
                    <div class="chart-area">
                        <svg class="energy-curve" viewBox="0 0 100 100">
                            <path d="${pathData}" stroke="#4a90e2" stroke-width="2" fill="none"/>
                        </svg>
                        ${nodesHtml}
                    </div>
                    <div class="chart-axis">
                        <span class="axis-label-left">能量指数</span>
                        <span class="axis-label-bottom">年龄</span>
                    </div>
                </div>
                <div class="timeline-legend">
                    <span>💡 点击节点查看详细分析</span>
                </div>
            </div>
            
            <script>
                function showDayunDetails(nodeIndex) {
                    // 隐藏所有tooltip
                    document.querySelectorAll('.node-tooltip').forEach(tooltip => {
                        tooltip.style.display = 'none';
                    });
                    
                    // 显示选中的tooltip
                    const tooltip = document.getElementById('tooltip-' + nodeIndex);
                    if (tooltip) {
                        tooltip.style.display = 'block';
                        
                        // 3秒后自动隐藏
                        setTimeout(() => {
                            tooltip.style.display = 'none';
                        }, 5000);
                    }
                }
            </script>
        `;
    }
    
    renderJujuDetection(jujuInfo) {
        const primaryTypes = jujuInfo['主要类型'] || [];
        const candidates = jujuInfo['候选类型'] || [];
        const plainDescriptions = jujuInfo['plain_descriptions'] || {};
        
        // 主要类型的通俗解释
        let primaryTypesHtml = '';
        if (primaryTypes.length > 0) {
            primaryTypesHtml = primaryTypes.map(type => {
                const description = plainDescriptions[type];
                return `
                    <div class="juju-type-card">
                        <div class="type-header">
                            <span class="primary-type">${type}</span>
                            ${description ? `<span class="type-icon">${description['鲜明标志'] || '⭐'}</span>` : ''}
                        </div>
                        ${description ? `
                            <div class="type-description">
                                <p class="core-trait"><strong>核心特点：</strong>${description['核心特点']}</p>
                                <p class="personality"><strong>性格表现：</strong>${description['性格表现']}</p>
                                <p class="behavior"><strong>典型行为：</strong>${description['典型行为']}</p>
                            </div>
                        ` : ''}
                    </div>
                `;
            }).join('');
        } else {
            primaryTypesHtml = '<p>暂无明确主类型</p>';
        }
        
        // 候选类型
        let candidatesHtml = '';
        if (candidates.length > 0) {
            candidatesHtml = `
                <div class="candidate-types">
                    <h4>🔍 其他可能的特征</h4>
                    <div class="candidate-list">
                        ${candidates.slice(0, 3).map(candidate => `
                            <span class="candidate-type">${candidate.type}</span>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        return `
            <div class="result-item juju-detection">
                <h3><i class="fas fa-user-tag"></i> 您的命局类型</h3>
                <div class="content">
                    <div class="primary-types">
                        <h4>🎯 主要类型分析</h4>
                        ${primaryTypesHtml}
                    </div>
                    ${candidatesHtml}
                    <div class="juju-note">
                        <p>💡 <strong>说明：</strong>命局类型反映了您天生的能量模式和性格倾向，了解这些特点可以帮助您更好地发挥优势、规避短板。</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    renderEnergyPortrait(portraitInfo) {
        return `
            <div class="result-item energy-portrait">
                <h3><i class="fas fa-portrait"></i> 您的能量画像</h3>
                <div class="content">
                    <div class="core-image">
                        <h4>核心意象</h4>
                        <p class="portrait-text">${portraitInfo['核心意象'] || ''}</p>
                    </div>
                    <div class="detailed-desc">
                        <h4>详细描述</h4>
                        <p>${portraitInfo['详细描述'] || ''}</p>
                    </div>
                    <div class="life-manifestation">
                        <h4>生活中的体现</h4>
                        <p>${portraitInfo['生活体现'] || ''}</p>
                    </div>
                    <div class="inner-voice">
                        <h4>内心的声音</h4>
                        <blockquote>"${portraitInfo['内心声音'] || ''}"</blockquote>
                    </div>
                    <div class="energy-rhythm">
                        <h4>能量节奏</h4>
                        <p>${portraitInfo['能量节奏'] || ''}</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    renderQuestionAnalysis(questionInfo) {
        const reflectionQuestions = questionInfo['深层反思问题'] || [];
        
        return `
            <div class="result-item question-analysis">
                <h3><i class="fas fa-lightbulb"></i> 关于您的问题</h3>
                <div class="content">
                    <div class="original-question">
                        <p><strong>您的问题：</strong>"${questionInfo['原始问题'] || ''}"</p>
                    </div>
                    <div class="deep-motivation">
                        <h4>问题背后的深层动机</h4>
                        <p>${questionInfo['深层动机'] || ''}</p>
                    </div>
                    <div class="why-important">
                        <h4>为什么这个问题对您很重要</h4>
                        <p>${questionInfo['重要性分析'] || ''}</p>
                    </div>
                    <div class="core-issue">
                        <h4>核心议题</h4>
                        <p>${questionInfo['核心议题'] || ''}</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    renderInspirationGuide(inspirationInfo) {
        const deeperQuestions = inspirationInfo['深层反思问题'] || [];
        const multipleAngles = inspirationInfo['多角度思考'] || [];
        const wisdomInsights = inspirationInfo['智慧洞察'] || [];
        
        return `
            <div class="result-item inspiration-guide">
                <h3><i class="fas fa-compass"></i> 更高维度的思考</h3>
                <div class="content">
                    <div class="reframed-perspective">
                        <h4>🔄 换个角度看问题</h4>
                        <p>${inspirationInfo['重新框定的视角'] || ''}</p>
                    </div>
                    
                    ${deeperQuestions.length > 0 ? `
                        <div class="deeper-questions">
                            <h4>🤔 值得深思的问题</h4>
                            <ul>
                                ${deeperQuestions.map(q => `<li>${q}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${multipleAngles.length > 0 ? `
                        <div class="multiple-angles">
                            <h4>🌟 多维度思考</h4>
                            <ul>
                                ${multipleAngles.map(angle => `<li>${angle}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${wisdomInsights.length > 0 ? `
                        <div class="wisdom-insights">
                            <h4>💡 智慧洞察</h4>
                            ${wisdomInsights.map(insight => `<blockquote>💭 ${insight}</blockquote>`).join('')}
                        </div>
                    ` : ''}
                    
                    <div class="consciousness-elevation">
                        <h4>⬆️ 意识层次的提升</h4>
                        <p>${inspirationInfo['意识提升'] || ''}</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    renderPersonalizedSolution(solutionInfo) {
        const strengthPatterns = solutionInfo['优势模式'] || [];
        const blindSpots = solutionInfo['温馨提醒'] || [];
        const actionableSteps = solutionInfo['行动建议'] || [];
        const medicineGuidance = solutionInfo['用药指导'] || {};
        
        return `
            <div class="result-item personalized-solution">
                <h3><i class="fas fa-key"></i> 破解的关键</h3>
                <div class="content">
                    ${strengthPatterns.length > 0 ? `
                        <div class="strength-patterns">
                            <h4>🌟 您的优势模式</h4>
                            <ul>
                                ${strengthPatterns.map(pattern => `<li>✨ ${pattern}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${blindSpots.length > 0 ? `
                        <div class="gentle-reminders">
                            <h4>💝 温馨提醒</h4>
                            <ul>
                                ${blindSpots.map(spot => `<li>💡 ${spot}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${actionableSteps.length > 0 ? `
                        <div class="actionable-steps">
                            <h4>📋 具体行动建议</h4>
                            <ol>
                                ${actionableSteps.map(step => `<li>▶️ ${step}</li>`).join('')}
                            </ol>
                        </div>
                    ` : ''}
                    
                    ${Object.keys(medicineGuidance).length > 0 ? `
                        <div class="medicine-guidance">
                            <h4>💊 意识能量调节</h4>
                            ${Object.entries(medicineGuidance).map(([type, guidance]) => 
                                `<p><strong>🔹 ${type}:</strong> ${guidance}</p>`
                            ).join('')}
                        </div>
                    ` : ''}
                    
                    <div class="timing-advice">
                        <h4>⏰ 时机把握</h4>
                        <p>🕐 ${solutionInfo['时机建议'] || '把握当下，顺应自然节奏'}</p>
                    </div>
                    
                    <div class="energy-management">
                        <h4>⚡ 能量管理</h4>
                        <p>🔋 ${solutionInfo['能量管理'] || '保持身心平衡，适度调节'}</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    renderEnhancedBingyao(enhancedBingyao) {
        const dualRoots = enhancedBingyao['双重病根分析'] || [];
        const medicineStrategy = enhancedBingyao['综合用药策略'] || {};
        
        return `
            <div class="result-item enhanced-bingyao">
                <h3><i class="fas fa-heartbeat"></i> 深度病药分析</h3>
                <div class="content">
                    ${dualRoots.length > 0 ? `
                        <div class="dual-roots">
                            <h4>病根分析</h4>
                            ${dualRoots.map(root => `
                                <div class="root-item">
                                    <h5>${root['病根类型']}</h5>
                                    <p><strong>具体表现：</strong>${root['具体表现']}</p>
                                    <p><strong>需要的药：</strong>${root['需要的药']}</p>
                                    <p><strong>生活体现：</strong>${root['生活体现']}</p>
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                    
                    ${Object.keys(medicineStrategy).length > 0 ? `
                        <div class="medicine-strategy">
                            <h4>用药策略</h4>
                            ${Object.entries(medicineStrategy).map(([level, info]) => `
                                <div class="medicine-level">
                                    <h5>${level}: ${info['药名']}</h5>
                                    <p><strong>意识指导：</strong>${info['意识指导']}</p>
                                    <p><strong>实践建议：</strong>${info['实践建议']}</p>
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }
    
    renderPlainLanguageSummary(plainSummary) {
        return `
            <div class="result-item plain-summary">
                <h3><i class="fas fa-comment-dots"></i> 大白话总结</h3>
                <div class="content">
                    ${plainSummary['格局说明'] ? `<p><strong>性格特点：</strong>${plainSummary['格局说明']}</p>` : ''}
                    ${plainSummary['五行说明'] ? `<p><strong>五行特质：</strong>${plainSummary['五行说明']}</p>` : ''}
                    ${plainSummary['调候说明'] ? `<p><strong>性格倾向：</strong>${plainSummary['调候说明']}</p>` : ''}
                    ${plainSummary['大运说明'] ? `<p><strong>时机分析：</strong>${plainSummary['大运说明']}</p>` : ''}
                </div>
            </div>
        `;
    }
    
    // 五行关系图交互功能
    addWuxingChartInteractivity(svgId) {
        // 延迟执行，等待DOM更新
        setTimeout(() => {
            const svg = document.getElementById(svgId);
            if (!svg) return;
            
            // 节点悬停效果
            const nodes = svg.querySelectorAll('.element-node');
            nodes.forEach(node => {
                const element = node.getAttribute('data-element');
                
                node.addEventListener('mouseenter', () => {
                    // 高亮相关连线
                    const relatedLines = svg.querySelectorAll(`line[x1][y1][x2][y2]`);
                    relatedLines.forEach(line => {
                        const desc = line.getAttribute('data-description') || '';
                        if (desc.includes(node.textContent.trim())) {
                            line.style.opacity = '1';
                            line.style.strokeWidth = (parseFloat(line.getAttribute('stroke-width')) * 1.5) + 'px';
                        } else {
                            line.style.opacity = '0.3';
                        }
                    });
                    
                    // 节点高亮
                    node.style.filter = 'brightness(1.3) drop-shadow(0 0 10px currentColor)';
                });
                
                node.addEventListener('mouseleave', () => {
                    // 恢复所有连线
                    const allLines = svg.querySelectorAll('line');
                    allLines.forEach(line => {
                        line.style.opacity = '0.7';
                        line.style.strokeWidth = line.getAttribute('stroke-width');
                    });
                    
                    // 恢复节点
                    node.style.filter = '';
                });
            });
            
            // 连线悬停效果
            const lines = svg.querySelectorAll('.relation-line');
            lines.forEach(line => {
                line.addEventListener('mouseenter', () => {
                    line.style.opacity = '1';
                    line.style.filter = 'drop-shadow(0 0 8px currentColor)';
                    
                    // 创建临时提示框
                    const tooltip = document.createElement('div');
                    tooltip.className = 'wuxing-tooltip';
                    tooltip.textContent = line.getAttribute('data-description');
                    tooltip.style.cssText = `
                        position: absolute;
                        background: rgba(0,0,0,0.8);
                        color: white;
                        padding: 8px 12px;
                        border-radius: 6px;
                        font-size: 14px;
                        pointer-events: none;
                        z-index: 1000;
                        white-space: nowrap;
                    `;
                    document.body.appendChild(tooltip);
                    
                    line._tooltip = tooltip;
                });
                
                line.addEventListener('mousemove', (e) => {
                    if (line._tooltip) {
                        line._tooltip.style.left = (e.pageX + 10) + 'px';
                        line._tooltip.style.top = (e.pageY - 30) + 'px';
                    }
                });
                
                line.addEventListener('mouseleave', () => {
                    line.style.opacity = '0.7';
                    line.style.filter = '';
                    
                    if (line._tooltip) {
                        document.body.removeChild(line._tooltip);
                        line._tooltip = null;
                    }
                });
            });
        }, 100);
    }
    
    renderWuxingRelationshipChart(wuxingData) {
        const nodes = wuxingData.relationship_graph?.nodes || [];
        const edges = wuxingData.relationship_graph?.edges || [];
        const breakpoints = wuxingData.breakpoints || [];
        const flowAnalysis = wuxingData.flow_analysis || {};
        
        // 创建互动式五行关系图
        const svgId = 'wuxing-chart-' + Date.now();
        
        return `
            <div class="result-item wuxing-relationship">
                <h3><i class="fas fa-project-diagram"></i> 五行能量关系图</h3>
                <div class="content">
                    <!-- 流动质量总览 -->
                    <div class="flow-overview">
                        <div class="flow-quality-indicator">
                            <span class="quality-label">能量流动质量:</span>
                            <span class="quality-value ${flowAnalysis.flow_quality === '顺畅' ? 'good' : flowAnalysis.flow_quality === '阻滞' ? 'poor' : 'average'}">
                                ${flowAnalysis.flow_quality || '正常'}
                            </span>
                            <span class="flow-strength">(强度: ${Math.round((flowAnalysis.overall_flow_strength || 1) * 100)}%)</span>
                        </div>
                    </div>
                    
                    <!-- SVG 五行关系图 -->
                    <div class="wuxing-chart-container">
                        <svg id="${svgId}" width="500" height="400" viewBox="0 0 500 400" class="wuxing-svg">
                            <!-- 定义箭头标记 -->
                            <defs>
                                <marker id="generate-arrow" markerWidth="10" markerHeight="10" 
                                        refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
                                    <path d="M0,0 L0,6 L9,3 z" fill="#4ade80"/>
                                </marker>
                                <marker id="overcome-arrow" markerWidth="10" markerHeight="10" 
                                        refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
                                    <path d="M0,0 L0,6 L9,3 z" fill="#f87171"/>
                                </marker>
                            </defs>
                            
                            <!-- 五行节点 -->
                            ${nodes.map((node, index) => {
                                const angle = (index * 2 * Math.PI) / 5 - Math.PI / 2; // 从顶部开始
                                const radius = 120;
                                const x = 250 + radius * Math.cos(angle);
                                const y = 200 + radius * Math.sin(angle);
                                const size = Math.max(20, Math.min(60, node.size || 30));
                                
                                return `
                                    <g class="element-node" data-element="${node.id}">
                                        <circle cx="${x}" cy="${y}" r="${size}" 
                                                fill="${node.color}" opacity="0.8" 
                                                stroke="#333" stroke-width="2"
                                                class="node-circle" />
                                        <text x="${x}" y="${y + 5}" text-anchor="middle" 
                                              font-size="16" font-weight="bold" fill="white">
                                            ${node.name}
                                        </text>
                                        <text x="${x}" y="${y + 25}" text-anchor="middle" 
                                              font-size="12" fill="white">
                                            ${node.energy}
                                        </text>
                                    </g>
                                `;
                            }).join('')}
                            
                            <!-- 关系连线 -->
                            ${edges.map(edge => {
                                const fromNode = nodes.find(n => n.id === edge.from);
                                const toNode = nodes.find(n => n.id === edge.to);
                                if (!fromNode || !toNode) return '';
                                
                                const fromIndex = nodes.indexOf(fromNode);
                                const toIndex = nodes.indexOf(toNode);
                                const fromAngle = (fromIndex * 2 * Math.PI) / 5 - Math.PI / 2;
                                const toAngle = (toIndex * 2 * Math.PI) / 5 - Math.PI / 2;
                                const radius = 120;
                                
                                const x1 = 250 + radius * Math.cos(fromAngle);
                                const y1 = 200 + radius * Math.sin(fromAngle);
                                const x2 = 250 + radius * Math.cos(toAngle);
                                const y2 = 200 + radius * Math.sin(toAngle);
                                
                                const strokeWidth = Math.max(1, Math.min(6, edge.width || 2));
                                const markerEnd = edge.type === 'generate' ? 'url(#generate-arrow)' : 'url(#overcome-arrow)';
                                
                                return `
                                    <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"
                                          stroke="${edge.color}" stroke-width="${strokeWidth}"
                                          stroke-dasharray="${edge.style === 'dashed' ? '5,5' : 'none'}"
                                          marker-end="${markerEnd}"
                                          class="relation-line ${edge.type}"
                                          data-description="${edge.description}">
                                        <title>${edge.description}</title>
                                    </line>
                                `;
                            }).join('')}
                        </svg>
                    </div>
                    
                    <!-- 能量断点提示 -->
                    ${breakpoints.length > 0 ? `
                        <div class="breakpoints-section">
                            <h4><i class="fas fa-exclamation-triangle"></i> 能量断点分析</h4>
                            <div class="breakpoints-grid">
                                ${breakpoints.map(bp => `
                                    <div class="breakpoint-card">
                                        <div class="bp-header">
                                            <span class="bp-element">${bp.element_name}</span>
                                            <span class="bp-type ${bp.break_type}">${bp.break_type}</span>
                                        </div>
                                        <div class="bp-remedy">
                                            <strong>化解方案:</strong> 加强 ${bp.remedy_names.join('、')} 能量
                                        </div>
                                        <div class="bp-impact">
                                            影响程度: ${bp.impact_level >= 0.8 ? '高' : bp.impact_level >= 0.5 ? '中' : '低'}
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                    
                    <!-- 交互说明 -->
                    <div class="chart-instructions">
                        <p><i class="fas fa-info-circle"></i> 鼠标悬停在节点和连线上可查看详细信息</p>
                        <div class="legend">
                            <div class="legend-item">
                                <div class="legend-line generate"></div>
                                <span>相生关系 (实线绿色)</span>
                            </div>
                            <div class="legend-item">
                                <div class="legend-line overcome"></div>
                                <span>相克关系 (虚线红色)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // 添加交互功能
        this.addWuxingChartInteractivity(svgId);
        
        return html;
    }

    showError(message) {
        this.hideLoading();
        alert(`错误: ${message}`);
        this.showInputSection();
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM加载完成，初始化应用');
    try {
        new BaziApp();
    } catch (error) {
        console.error('应用初始化失败:', error);
    }
});