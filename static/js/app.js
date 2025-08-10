// 八字能量解读系统 - 主要JavaScript代码
class BaziApp {
    constructor() {
        console.log('BaziApp 初始化开始');
        this.initializeElements();
        this.bindEvents();
        this.showInputSection();
        console.log('BaziApp 初始化完成');
    }

    initializeElements() {
        console.log('开始获取页面元素...');
        
        this.form = document.getElementById('baziForm');
        this.nameInput = document.getElementById('name');
        this.genderInput = document.getElementById('gender');
        this.birthYearInput = document.getElementById('birth_year');
        this.birthMonthInput = document.getElementById('birth_month');
        this.birthDayInput = document.getElementById('birth_day');
        this.birthHourInput = document.getElementById('birth_hour');
        this.birthMinuteInput = document.getElementById('birth_minute');
        this.locationInput = document.getElementById('location');
        this.questionInput = document.getElementById('question');
        this.submitBtn = document.getElementById('submitBtn');
        this.loading = document.getElementById('loading');
        this.resultSection = document.getElementById('resultSection');
        this.resultContent = document.getElementById('resultContent');
        this.newAnalysisBtn = document.getElementById('newAnalysis');
        this.inputSection = document.querySelector('.input-section');
        
        // 检查关键元素是否正确获取
        console.log('元素获取结果:', {
            form: !!this.form,
            nameInput: !!this.nameInput,
            submitBtn: !!this.submitBtn,
            表单ID: this.form?.id,
            按钮ID: this.submitBtn?.id,
            按钮类型: this.submitBtn?.type
        });
        
        // 检查是否有缺失的元素
        const missingElements = [];
        if (!this.form) missingElements.push('baziForm');
        if (!this.submitBtn) missingElements.push('submitBtn');
        if (!this.nameInput) missingElements.push('name');
        
        if (missingElements.length > 0) {
            console.error('缺失的页面元素:', missingElements);
        }
    }

    bindEvents() {
        console.log('开始绑定事件...');
        
        // 表单提交事件
        if (this.form) {
            this.form.addEventListener('submit', (e) => {
                console.log('表单提交事件被触发!');
                this.handleSubmit(e);
            });
            console.log('表单提交事件绑定成功');
        } else {
            console.error('表单元素不存在，无法绑定提交事件');
        }
        
        // 重新分析按钮事件
        if (this.newAnalysisBtn) {
            this.newAnalysisBtn.addEventListener('click', () => this.showInputSection());
            console.log('重新分析按钮事件绑定成功');
        }
        
        // 简单的按钮点击测试
        if (this.submitBtn) {
            this.submitBtn.addEventListener('click', (e) => {
                console.log('按钮直接点击事件触发!', e.type);
            });
            console.log('按钮点击事件绑定成功');
        }
        
        console.log('所有事件绑定完成');
    }

    validateForm() {
        // 只在提交时进行严格验证，平时不禁用按钮
        const name = this.nameInput.value.trim();
        const gender = this.genderInput.value;
        const birthYear = this.birthYearInput.value;
        const birthMonth = this.birthMonthInput.value;
        const birthDay = this.birthDayInput.value;
        const birthHour = this.birthHourInput.value;
        
        console.log('表单验证:', {name, gender, birthYear, birthMonth, birthDay, birthHour});
        
        const isValid = name && gender && birthYear && birthMonth && birthDay && birthHour;
        
        // 不在这里禁用按钮，让用户随时可以尝试提交
        // this.submitBtn.disabled = !isValid;
        
        console.log('表单是否有效:', isValid);
        
        return isValid;
    }

    async handleSubmit(e) {
        e.preventDefault();
        console.log('表单提交事件触发');
        
        if (!this.validateForm()) {
            console.log('表单验证失败');
            this.showError('请填写完整的个人信息');
            return;
        }
        
        console.log('表单验证通过，开始提交');

        const formData = {
            name: this.nameInput.value.trim(),
            gender: this.genderInput.value,
            birth_year: parseInt(this.birthYearInput.value),
            birth_month: parseInt(this.birthMonthInput.value),
            birth_day: parseInt(this.birthDayInput.value),
            birth_hour: parseInt(this.birthHourInput.value),
            birth_minute: parseInt(this.birthMinuteInput.value) || 0,
            location: this.locationInput.value.trim() || '北京',
            question: this.questionInput.value.trim()
        };

        this.showLoading();
        
        try {
            const result = await this.submitForAnalysis(formData);
            this.displayResult(result);
        } catch (error) {
            this.showError(error.message);
        }
    }

    async submitForAnalysis(formData) {
        const response = await fetch('/interpret', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '分析失败，请重试');
        }

        const data = await response.json();
        if (!data.ok) {
            throw new Error('分析失败，请重试');
        }

        return data.result;
    }

    displayResult(result) {
        this.hideLoading();
        this.showResultSection();
        
        let html = '';
        
        // 用户信息展示
        if (result['用户信息']) {
            html += this.renderUserInfo(result['用户信息']);
        }
        
        // 八字信息展示
        if (result['bazi']) {
            html += this.renderBaziInfo(result['bazi']);
        }
        
        // 五行统计
        if (result['五行统计']) {
            html += this.renderElementsChart(result['五行统计']);
        }
        
        // 格局分析
        if (result['定格局']) {
            html += this.renderGeJuAnalysis(result['定格局']);
        }
        
        // 寒燥分析
        if (result['定寒燥']) {
            html += this.renderHanZaoAnalysis(result['定寒燥']);
        }
        
        // 病药分析 - 这是新增的重点功能
        if (result['定病药']) {
            html += this.renderBingYaoAnalysis(result['定病药']);
        }
        
        // 大运分析
        if (result['看大运']) {
            html += this.renderDayunAnalysis(result['看大运']);
        }
        
        // 五行生克关系
        if (result['五行生克关系']) {
            html += this.renderWuXingRelations(result['五行生克关系']);
        }
        
        // 问题回答
        if (result['问题']) {
            html += this.renderQuestionAnswer(result['问题']);
        }
        
        this.resultContent.innerHTML = html;
    }

    renderUserInfo(userInfo) {
        return `
            <div class="result-item user-info">
                <h3><i class="fas fa-user"></i> 用户信息</h3>
                <div class="content">
                    <div class="info-grid">
                        <div><strong>姓名：</strong>${userInfo['姓名']}</div>
                        <div><strong>性别：</strong>${userInfo['性别']}</div>
                        <div><strong>出生时间：</strong>${userInfo['出生时间']}</div>
                        <div><strong>出生地点：</strong>${userInfo['出生地点']}</div>
                    </div>
                </div>
            </div>
        `;
    }

    renderBaziInfo(baziInfo) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-calendar-alt"></i> 八字信息</h3>
                <div class="bazi-display">
                    <div class="pillar">
                        <div class="pillar-label">年柱</div>
                        <div class="pillar-text">${baziInfo['year']}</div>
                    </div>
                    <div class="pillar">
                        <div class="pillar-label">月柱</div>
                        <div class="pillar-text">${baziInfo['month']}</div>
                    </div>
                    <div class="pillar">
                        <div class="pillar-label">日柱</div>
                        <div class="pillar-text">${baziInfo['day']}</div>
                    </div>
                    <div class="pillar">
                        <div class="pillar-label">时柱</div>
                        <div class="pillar-text">${baziInfo['hour']}</div>
                    </div>
                </div>
            </div>
        `;
    }

    renderElementsChart(elements) {
        const elementMap = {
            'wood': '木',
            'fire': '火', 
            'earth': '土',
            'metal': '金',
            'water': '水'
        };

        return `
            <div class="result-item">
                <h3><i class="fas fa-chart-bar"></i> 五行统计</h3>
                <div class="elements-chart">
                    ${Object.entries(elements).map(([element, count]) => {
                        if (element === '最旺' || element === '最弱') return '';
                        return `
                            <div class="element-bar ${element}">
                                <div class="element-name">${elementMap[element] || element}</div>
                                <div class="element-count">${count}</div>
                            </div>
                        `;
                    }).join('')}
                </div>
                <p><strong>最旺：</strong>${elementMap[elements['最旺']] || elements['最旺']}</p>
                <p><strong>最弱：</strong>${elementMap[elements['最弱']] || elements['最弱']}</p>
            </div>
        `;
    }

    renderGeJuAnalysis(geju) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-chess"></i> 格局分析</h3>
                <div class="content">
                    <p><strong>格局类型：</strong>${geju['格局类型']}</p>
                    <p><strong>强弱：</strong>${geju['强弱']}</p>
                    <p><strong>根：</strong>${geju['根']}</p>
                    <p><strong>扶抑关系：</strong>${geju['扶抑关系']}</p>
                </div>
            </div>
        `;
    }

    renderHanZaoAnalysis(hanzao) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-thermometer-half"></i> 寒燥分析</h3>
                <div class="content">
                    <p><strong>类型：</strong>${hanzao['类型']}</p>
                    <p><strong>原因：</strong>${hanzao['原因']}</p>
                    <p><strong>需要调候：</strong>${hanzao['需要调候']}</p>
                    <p><strong>调候药效顺序：</strong>${hanzao['调候药效顺序'].join(' → ')}</p>
                </div>
            </div>
        `;
    }

    renderBingYaoAnalysis(bingyao) {
        if (!bingyao['分级'] || !bingyao['分级'][0]) return '';
        
        const analysis = bingyao['分级'][0];
        
        return `
            <div class="result-item bingyao-analysis">
                <h3><i class="fas fa-pills"></i> 病药体系分析</h3>
                <div class="content">
                    <div class="pattern-info">
                        <h4>命局诊断</h4>
                        <p><strong>命局类型：</strong><span class="pattern-type">${analysis['命局类型']}</span></p>
                        <p><strong>命局描述：</strong>${analysis['命局描述']}</p>
                        <p><strong>能量本质：</strong>${analysis['能量本质']}</p>
                        <p><strong>关系类型：</strong>${analysis['关系类型']}</p>
                    </div>
                    
                    <div class="medicine-config">
                        <h4>病药配置</h4>
                        <div class="medicine-grid">
                            <div class="medicine-item chief">
                                <div class="medicine-label">君药</div>
                                <div class="medicine-name">${analysis['病药配置']['君药']}</div>
                            </div>
                            <div class="medicine-item minister">
                                <div class="medicine-label">臣药</div>
                                <div class="medicine-name">${analysis['病药配置']['臣药']}</div>
                            </div>
                            <div class="medicine-item assistant">
                                <div class="medicine-label">次药</div>
                                <div class="medicine-name">${analysis['病药配置']['次药']}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="medicine-effectiveness">
                        <h4>药效分析</h4>
                        ${Object.entries(analysis['药效分析']).map(([level, effect]) => `
                            <p><strong>${level}：</strong>${effect}</p>
                        `).join('')}
                    </div>
                    
                    <div class="consciousness">
                        <h4>意识特质</h4>
                        <p>${analysis['意识特质']}</p>
                    </div>
                </div>
            </div>
        `;
    }

    renderDayunAnalysis(dayun) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-road"></i> 大运分析</h3>
                <div class="content">
                    <div class="current-luck">
                        <h4>当前大运 (${dayun['当前大运']['age_range']}岁)</h4>
                        <p><strong>干支：</strong>${dayun['当前大运']['gan']}${dayun['当前大运']['zhi']}</p>
                        <p><strong>影响：</strong>${dayun['当前大运']['influence']}</p>
                    </div>
                    
                    <div class="future-luck">
                        <h4>未来大运</h4>
                        ${dayun['未来大运'].map(period => `
                            <div class="luck-period">
                                <strong>${period['age_range']}岁：</strong>
                                ${period['gan']}${period['zhi']} - ${period['influence']}
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    renderWuXingRelations(relations) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-project-diagram"></i> 五行生克关系</h3>
                <div class="content">
                    <p><strong>总结：</strong>${relations['summary']}</p>
                    <p><strong>循环状况：</strong>${relations['flow_analysis']['flow_quality']}</p>
                    <p><strong>整体流畅度：</strong>${(relations['flow_analysis']['overall_flow_strength'] * 100).toFixed(1)}%</p>
                </div>
            </div>
        `;
    }

    renderQuestionAnswer(question) {
        if (!question) return '';
        
        return `
            <div class="result-item question-answer">
                <h3><i class="fas fa-question-circle"></i> 针对性解答</h3>
                <div class="content">
                    <div class="question-text">
                        <strong>您的问题：</strong>${question}
                    </div>
                    <div class="answer-text">
                        <p>基于您的八字分析和病药体系，系统将为您提供针对性的建议和指导。</p>
                    </div>
                </div>
            </div>
        `;
    }

    showInputSection() {
        this.inputSection.style.display = 'block';
        this.resultSection.style.display = 'none';
        this.loading.style.display = 'none';
        
        // 重置表单
        this.form.reset();
        
        // 初始化时不禁用按钮
        this.submitBtn.disabled = false;
    }

    showLoading() {
        this.inputSection.style.display = 'none';
        this.resultSection.style.display = 'none';
        this.loading.style.display = 'block';
    }

    hideLoading() {
        this.loading.style.display = 'none';
    }

    showResultSection() {
        this.inputSection.style.display = 'none';
        this.resultSection.style.display = 'block';
    }

    showError(message) {
        this.hideLoading();
        alert(`错误: ${message}`);
        this.showInputSection();
    }
}

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM内容加载完成');
    const app = new BaziApp();
    
    // 测试按钮点击
    setTimeout(() => {
        const btn = document.getElementById('submitBtn');
        console.log('按钮状态检查:', {
            元素存在: !!btn,
            disabled: btn?.disabled,
            样式: btn?.style.cssText,
            类名: btn?.className
        });
    }, 1000);
});

// 实用工具函数
const Utils = {
    // 格式化日期
    formatDate(date) {
        return new Intl.DateTimeFormat('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(date);
    },
    
    // 防抖函数
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};