// 增强版八字能量分析系统前端应用

class EnhancedBaziApp {
    constructor() {
        this.currentMode = 'main-input';
        this.currentAnalysisData = null;
        this.isExpertView = false;
        
        this.initializeElements();
        this.bindEvents();
        this.setupLoadingAnimation();
        this.setupAutoAgeCalculation();
    }

    initializeElements() {
        // 简化的表单元素
        this.mainForm = document.getElementById('mainForm');
        
        // 表单字段
        this.nameInput = document.getElementById('name');
        this.genderInput = document.getElementById('gender');
        this.birthYearInput = document.getElementById('birth_year');
        this.birthMonthInput = document.getElementById('birth_month');
        this.birthDayInput = document.getElementById('birth_day');
        this.birthHourInput = document.getElementById('birth_hour');
        this.locationInput = document.getElementById('location');
        this.questionInput = document.getElementById('question');
        this.modeInput = document.getElementById('mode');
        this.llmOptionInput = document.getElementById('llm_option');
        this.currentAgeInput = document.getElementById('current_age');
        
        // 结果相关元素
        this.loading = document.getElementById('loading');
        this.resultSection = document.getElementById('resultSection');
        this.resultContent = document.getElementById('resultContent');
        
        // 操作按钮
        this.downloadPdfBtn = document.getElementById('downloadPdf');
        this.toggleExpertBtn = document.getElementById('toggleExpert');
        this.apiSettingsBtn = document.getElementById('apiSettings');
        this.newAnalysisBtn = document.getElementById('newAnalysis');
        
        // 模态框
        this.disclaimerModal = document.getElementById('disclaimerModal');
        this.apiSettingsModal = document.getElementById('apiSettingsModal');
        
        // API设置相关元素
        this.apiConfigForm = document.getElementById('apiConfigForm');
        this.apiStatusDiv = document.getElementById('apiStatus');
        this.testApiBtn = document.getElementById('testApiBtn');
    }

    bindEvents() {
        // 主表单提交
        if (this.mainForm) {
            this.mainForm.addEventListener('submit', (e) => this.handleMainFormSubmit(e));
        }

        // 示例按钮
        document.querySelectorAll('.example-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleExampleClick(e));
        });

        // 结果操作按钮
        if (this.downloadPdfBtn) {
            this.downloadPdfBtn.addEventListener('click', () => this.downloadPDF());
        }
        
        if (this.toggleExpertBtn) {
            this.toggleExpertBtn.addEventListener('click', () => this.toggleExpertView());
        }
        
        if (this.apiSettingsBtn) {
            this.apiSettingsBtn.addEventListener('click', () => this.showApiSettings());
        }
        
        if (this.newAnalysisBtn) {
            this.newAnalysisBtn.addEventListener('click', () => this.showInputSection(this.currentMode));
        }

        // API设置表单事件
        if (this.apiConfigForm) {
            this.apiConfigForm.addEventListener('submit', (e) => this.handleApiConfigSubmit(e));
        }
        
        if (this.testApiBtn) {
            this.testApiBtn.addEventListener('click', () => this.testApiConnection());
        }

        // 模态框事件
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-close') || e.target.classList.contains('modal')) {
                this.closeModal();
            }
        });

        // 年龄自动计算
        [this.birthYearInput, this.birthMonthInput, this.birthDayInput].forEach(input => {
            if (input) {
                input.addEventListener('change', () => this.updateAge());
            }
        });
    }
    
    setupAutoAgeCalculation() {
        // 初始化时计算一次年龄
        this.updateAge();
    }
    
    updateAge() {
        if (!this.birthYearInput || !this.birthMonthInput || !this.birthDayInput || !this.currentAgeInput) return;
        
        const year = parseInt(this.birthYearInput.value);
        const month = parseInt(this.birthMonthInput.value);
        const day = parseInt(this.birthDayInput.value);
        
        if (year && month && day) {
            const today = new Date();
            let age = today.getFullYear() - year;
            
            // 如果今年的生日还没到，年龄减1
            if (today.getMonth() + 1 < month || (today.getMonth() + 1 === month && today.getDate() < day)) {
                age--;
            }
            
            this.currentAgeInput.value = Math.max(0, age);
        }
    }

    handleTabClick(e) {
        const tabId = e.currentTarget.getAttribute('data-tab');
        this.switchTab(tabId);
    }

    switchTab(tabId) {
        // 更新按钮状态
        this.tabBtns.forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
        });

        // 切换输入区域
        document.querySelectorAll('.input-section').forEach(section => {
            section.classList.toggle('active', section.id === tabId);
        });

        this.currentMode = tabId;
    }

    validateBaziInput() {
        const bazi = this.baziInput.value.trim();
        const pattern = /^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]\s+[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]\s+[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]\s+[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]$/;
        
        const submitBtn = this.baziForm.querySelector('.btn-primary');
        if (bazi && !pattern.test(bazi)) {
            this.baziInput.style.borderColor = '#ef4444';
            submitBtn.disabled = true;
        } else {
            this.baziInput.style.borderColor = '#e2e8f0';
            submitBtn.disabled = false;
        }
    }

    handleExampleClick(e) {
        const exampleData = e.target.getAttribute('data-example');
        if (exampleData) {
            try {
                const data = JSON.parse(exampleData);
                
                // 填充表单
                if (this.nameInput) this.nameInput.value = data.name || '';
                if (this.genderInput) this.genderInput.value = data.gender || '';
                if (this.birthYearInput) this.birthYearInput.value = data.year || 1990;
                if (this.birthMonthInput) this.birthMonthInput.value = data.month || 1;
                if (this.birthDayInput) this.birthDayInput.value = data.day || 1;
                if (this.birthHourInput) this.birthHourInput.value = data.hour || 12;
                if (this.locationInput) this.locationInput.value = data.location || '';
                
                // 更新年龄
                this.updateAge();
            } catch (e) {
                console.error('解析示例数据失败:', e);
            }
        }
    }
    
    async handleMainFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(this.mainForm);
        const requestData = {
            birth_info: {
                name: formData.get('name'),
                gender: formData.get('gender'),
                year: parseInt(formData.get('birth_year')),
                month: parseInt(formData.get('birth_month')),
                day: parseInt(formData.get('birth_day')),
                hour: parseInt(formData.get('birth_hour')),
                minute: 0,
                location: formData.get('location')
            },
            question: formData.get('question') || '',
            mode: formData.get('mode') || 'general',
            llm_option: formData.get('llm_option') || 'local',
            current_age: parseInt(formData.get('current_age')) || 25
        };

        await this.performAnalysis(requestData);
    }

    async handleBaziSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(this.baziForm);
        const requestData = {
            bazi_string: formData.get('bazi'),
            question: formData.get('question') || '',
            mode: formData.get('mode') || 'general',
            current_age: parseInt(formData.get('current_age')) || 25
        };

        await this.performAnalysis(requestData);
    }

    async handleBirthSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(this.birthForm);
        const requestData = {
            birth_info: {
                year: parseInt(formData.get('birth_year')),
                month: parseInt(formData.get('birth_month')),
                day: parseInt(formData.get('birth_day')),
                hour: parseInt(formData.get('birth_hour')),
                minute: 0,
                timezone: formData.get('timezone') || 'Asia/Shanghai',
                hemisphere: formData.get('hemisphere') || 'north',
                location: formData.get('location') || '',
                gender: formData.get('gender') || ''
            },
            question: formData.get('question') || '',
            mode: formData.get('mode') || 'general',
            current_age: parseInt(formData.get('current_age')) || 25
        };

        await this.performAnalysis(requestData);
    }

    async performAnalysis(requestData) {
        this.showLoading();
        
        try {
            const response = await fetch('/api/v2/comprehensive-analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || '分析失败，请重试');
            }

            const data = await response.json();
            if (!data.success) {
                throw new Error('分析失败，请重试');
            }

            this.currentAnalysisData = data.data;
            this.displayResult(data.data);
            
        } catch (error) {
            this.showError(error.message);
        }
    }

    showLoading() {
        document.querySelectorAll('.input-section').forEach(section => {
            section.style.display = 'none';
        });
        this.resultSection.style.display = 'none';
        this.loading.style.display = 'block';

        // 模拟加载步骤动画
        this.animateLoadingSteps();
    }

    animateLoadingSteps() {
        const steps = document.querySelectorAll('.loading-steps .step');
        steps.forEach((step, index) => {
            setTimeout(() => {
                steps.forEach(s => s.classList.remove('active'));
                step.classList.add('active');
            }, index * 800);
        });
    }

    hideLoading() {
        this.loading.style.display = 'none';
    }

    displayResult(data) {
        this.hideLoading();
        this.showResultSection();
        
        const structured = data.structured_analysis;
        const interpretation = data.natural_language_interpretation;
        const metadata = data.metadata || {};
        const mode = metadata.mode || 'general';
        
        let html = '';
        
        // 八字信息（包含藏干）
        html += this.renderBaziInfo(structured.bazi, mode);
        
        // 能量画像
        html += this.renderEnergyPortrait(interpretation.energy_portrait);
        
        // 问题回答
        if (interpretation.question_answer) {
            html += this.renderQuestionAnswer(interpretation.question_answer);
        }
        
        // 统一显示最详细的完整分析
        html += this.renderElementsChart(structured['五行统计']);
        html += this.renderGeJuAnalysis(structured['定格局']);
        html += this.renderHanZaoAnalysis(structured['定寒燥']);
        html += this.renderBingYaoAnalysis(structured['定病药']);
        html += this.renderDaYunAnalysis(structured['看大运']);
        
        // 五行生克关系分析
        if (structured['五行生克关系']) {
            html += this.renderWuxingRelations(structured['五行生克关系']);
        }
        if (structured['专家模式数据']) {
            html += this.renderExpertData(structured['专家模式数据']);
        }
        const llmOptionText = metadata.llm_option === 'claude_api' ? 'Claude API分析' : '本地AI分析';
        html += `<div class="mode-badge detailed-badge">
                    <i class="fas fa-microscope"></i> 完整详细分析 | ${llmOptionText}
                 </div>`;
        
        // 调候建议
        if (interpretation.practice_suggestions) {
            html += this.renderPracticeSuggestions(interpretation.practice_suggestions);
        }
        
        // 免责声明
        if (interpretation.disclaimer) {
            html += this.renderDisclaimer(interpretation.disclaimer);
        }
        
        this.resultContent.innerHTML = html;
    }

    renderBaziInfo(baziInfo, mode = 'detailed') {
        // 解析八字数据
        const pillars = [
            { label: '年柱', value: baziInfo.year },
            { label: '月柱', value: baziInfo.month },
            { label: '日柱', value: baziInfo.day },
            { label: '时柱', value: baziInfo.hour }
        ];
        
        // 提取天干和地支
        const tianGan = pillars.map(p => p.value.charAt(0));
        const diZhi = pillars.map(p => p.value.charAt(1));
        
        // 地支藏干映射（基于后端数据）
        const diZhiZangGan = {
            "子": [{"gan": "癸", "type": "主气"}],
            "丑": [{"gan": "己", "type": "主气"}, {"gan": "癸", "type": "中气"}, {"gan": "辛", "type": "余气"}],
            "寅": [{"gan": "甲", "type": "主气"}, {"gan": "丙", "type": "中气"}, {"gan": "戊", "type": "余气"}],
            "卯": [{"gan": "乙", "type": "主气"}],
            "辰": [{"gan": "戊", "type": "主气"}, {"gan": "乙", "type": "中气"}, {"gan": "癸", "type": "余气"}],
            "巳": [{"gan": "丙", "type": "主气"}, {"gan": "庚", "type": "中气"}, {"gan": "戊", "type": "余气"}],
            "午": [{"gan": "丁", "type": "主气"}, {"gan": "己", "type": "中气"}],
            "未": [{"gan": "己", "type": "主气"}, {"gan": "丁", "type": "中气"}, {"gan": "乙", "type": "余气"}],
            "申": [{"gan": "庚", "type": "主气"}, {"gan": "壬", "type": "中气"}, {"gan": "戊", "type": "余气"}],
            "酉": [{"gan": "辛", "type": "主气"}],
            "戌": [{"gan": "戊", "type": "主气"}, {"gan": "辛", "type": "中气"}, {"gan": "丁", "type": "余气"}],
            "亥": [{"gan": "壬", "type": "主气"}, {"gan": "甲", "type": "中气"}]
        };
        
        // 五行颜色映射
        const elementColors = {
            // 木 - 绿色
            '甲': '#22c55e', '乙': '#16a34a', '寅': '#22c55e', '卯': '#16a34a',
            // 火 - 红色
            '丙': '#ef4444', '丁': '#dc2626', '巳': '#ef4444', '午': '#dc2626',
            // 土 - 黄色
            '戊': '#eab308', '己': '#ca8a04', '辰': '#eab308', '戌': '#ca8a04', 
            '丑': '#eab308', '未': '#ca8a04',
            // 金 - 银灰色
            '庚': '#9ca3af', '辛': '#6b7280', '申': '#9ca3af', '酉': '#6b7280',
            // 水 - 蓝色
            '壬': '#3b82f6', '癸': '#1d4ed8', '亥': '#3b82f6', '子': '#1d4ed8'
        };
        
        // 生成天干行HTML
        const tianGanHtml = tianGan.map((gan, index) => {
            const color = elementColors[gan] || '#4a5568';
            return `<div class="bazi-char tiangan" style="color: ${color}; border-color: ${color}20;">${gan}</div>`;
        }).join('');
        
        // 生成地支行HTML
        const diZhiHtml = diZhi.map((zhi, index) => {
            const color = elementColors[zhi] || '#4a5568';
            return `<div class="bazi-char dizhi" style="color: ${color}; border-color: ${color}20;">${zhi}</div>`;
        }).join('');
        
        // 生成柱标签（添加空占位符来对齐grid）
        const labelHtml = '<div></div>' + pillars.map(p => `<div class="pillar-label">${p.label}</div>`).join('');
        
        let zangGanHtml = '';
        
        // 始终显示藏干信息
        {
            const zangGanRowHtml = diZhi.map((zhi, index) => {
                const zangGanList = diZhiZangGan[zhi] || [];
                const zangGanText = zangGanList.map(zg => {
                    const color = elementColors[zg.gan] || '#4a5568';
                    const typeText = zg.type === '主气' ? '主' : zg.type === '中气' ? '中' : '余';
                    return `<span style="color: ${color}; font-size: 0.7rem;">${zg.gan}<sub>${typeText}</sub></span>`;
                }).join(' ');
                return `<div class="zanggan-cell">${zangGanText}</div>`;
            }).join('');
            
            zangGanHtml = `
                <div class="bazi-row zanggan-row">
                    <div class="row-label">藏干</div>
                    <div class="zanggan-chars">${zangGanRowHtml}</div>
                </div>
            `;
        }
        
        return `
            <div class="result-item">
                <h3><i class="fas fa-calendar-alt"></i> 八字命盘</h3>
                <div class="traditional-bazi-display">
                    <div class="pillar-labels">${labelHtml}</div>
                    <div class="bazi-row tiangan-row">
                        <div class="row-label">天干</div>
                        <div class="bazi-chars">${tianGanHtml}</div>
                    </div>
                    <div class="bazi-row dizhi-row">
                        <div class="row-label">地支</div>
                        <div class="bazi-chars">${diZhiHtml}</div>
                    </div>
                    ${zangGanHtml}
                </div>
            </div>
        `;
    }

    renderEnergyPortrait(portrait) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-user"></i> 能量画像</h3>
                <div class="content">
                    <p>${portrait}</p>
                </div>
            </div>
        `;
    }

    renderElementsChart(elementsData) {
        const elementMap = {
            'wood': { name: '木', class: 'wood' },
            'fire': { name: '火', class: 'fire' },
            'earth': { name: '土', class: 'earth' },
            'metal': { name: '金', class: 'metal' },
            'water': { name: '水', class: 'water' }
        };

        let html = `
            <div class="result-item">
                <h3><i class="fas fa-chart-bar"></i> 五行统计</h3>
                <div class="elements-chart">
        `;
        
        Object.entries(elementMap).forEach(([key, element]) => {
            const count = elementsData[key] || 0;
            const isStrongest = key === elementsData['最旺'];
            const isWeakest = key === elementsData['最弱'];
            
            html += `
                <div class="element-bar ${element.class} ${isStrongest ? 'strongest' : ''} ${isWeakest ? 'weakest' : ''}">
                    <div class="element-name">${element.name}</div>
                    <div class="element-count">${count.toFixed(1)}</div>
                    ${isStrongest ? '<div class="badge strongest">最旺</div>' : ''}
                    ${isWeakest ? '<div class="badge weakest">最弱</div>' : ''}
                </div>
            `;
        });
        
        html += '</div></div>';
        return html;
    }

    renderGeJuAnalysis(gejuData) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-chess-king"></i> 格局分析</h3>
                <div class="content">
                    <p><strong>格局类型：</strong>${gejuData['格局类型']}</p>
                    <p><strong>强弱判定：</strong>${gejuData['强弱']}</p>
                    <p><strong>根的状态：</strong>${gejuData['根']}</p>
                    <p><strong>扶抑关系：</strong>${gejuData['扶抑关系']}</p>
                </div>
            </div>
        `;
    }

    renderHanZaoAnalysis(hanzaoData) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-thermometer-half"></i> 寒燥调候分析</h3>
                <div class="content">
                    <p><strong>寒燥类型：</strong>${hanzaoData['类型']}</p>
                    <p><strong>判定原因：</strong>${hanzaoData['原因']}</p>
                    <p><strong>调候需求：</strong>${hanzaoData['需要调候']}</p>
                    <p><strong>药效顺序：</strong>${hanzaoData['调候药效顺序'].join(' > ') || '无需调候'}</p>
                </div>
            </div>
        `;
    }

    renderBingYaoAnalysis(bingyaoData) {
        let html = `
            <div class="result-item">
                <h3><i class="fas fa-pills"></i> 病药分级</h3>
                <table class="expert-table">
                    <thead>
                        <tr>
                            <th>级别</th>
                            <th>五行</th>
                            <th>有无</th>
                            <th>旺相</th>
                            <th>意识特质</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        bingyaoData['分级'].forEach(item => {
            html += `
                <tr>
                    <td><strong>${item.level}</strong></td>
                    <td>${item.element_cn}</td>
                    <td>${item.has}</td>
                    <td>${item.prosperity}</td>
                    <td>${item.consciousness}</td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div>';
        return html;
    }

    renderDaYunAnalysis(dayunData) {
        const current = dayunData['当前大运'];
        return `
            <div class="result-item">
                <h3><i class="fas fa-clock"></i> 大运分析</h3>
                <div class="content">
                    <p><strong>当前大运：</strong>${current['age_range']}岁</p>
                    <p><strong>大运干支：</strong>${current['gan']}${current['zhi']}</p>
                    <p><strong>影响分析：</strong>${current['influence']}</p>
                </div>
            </div>
        `;
    }

    renderWuxingRelations(relationsData) {
        let html = `
            <div class="result-item">
                <h3><i class="fas fa-recycle"></i> 五行生克关系分析</h3>
                <div class="wuxing-relations-container">
        `;
        
        // 显示总结
        if (relationsData.summary) {
            html += `
                <div class="relations-summary">
                    <h4><i class="fas fa-chart-line"></i> 关系总结</h4>
                    <p>${relationsData.summary}</p>
                </div>
            `;
        }
        
        // 显示能量流动分析
        if (relationsData.flow_analysis) {
            const flow = relationsData.flow_analysis;
            html += `
                <div class="flow-analysis">
                    <h4><i class="fas fa-water"></i> 能量流动分析</h4>
                    <div class="flow-stats">
                        <span class="flow-quality ${flow.flow_quality}">流动状况: ${flow.flow_quality}</span>
                        <span class="circulation-health">循环健康度: ${flow.circulation_health}</span>
                    </div>
                </div>
            `;
        }
        
        // 显示断点能量
        if (relationsData.breakpoints && relationsData.breakpoints.length > 0) {
            html += `
                <div class="breakpoints-analysis">
                    <h4><i class="fas fa-exclamation-triangle"></i> 断点能量分析</h4>
                    <div class="breakpoints-list">
            `;
            
            relationsData.breakpoints.forEach(bp => {
                const impactLevel = bp.impact_level > 0.7 ? 'high' : bp.impact_level > 0.4 ? 'medium' : 'low';
                html += `
                    <div class="breakpoint-item ${impactLevel}-impact">
                        <div class="breakpoint-header">
                            <span class="element-name">${bp.element_name}</span>
                            <span class="break-type">${bp.break_type}</span>
                            <span class="impact-level">影响: ${(bp.impact_level * 100).toFixed(0)}%</span>
                        </div>
                        ${bp.remedy_names.length > 0 ? 
                            `<div class="remedy-suggestion">建议补强: ${bp.remedy_names.join(', ')}</div>` : 
                            ''
                        }
                    </div>
                `;
            });
            
            html += `
                    </div>
                </div>
            `;
        }
        
        // 显示生克关系列表
        if (relationsData.relations && relationsData.relations.length > 0) {
            html += `
                <div class="relations-list">
                    <h4><i class="fas fa-arrows-alt"></i> 生克关系详情</h4>
                    <div class="relations-grid">
            `;
            
            // 分组显示相生和相克关系
            const generateRelations = relationsData.relations.filter(r => r.relation_type === 'generate');
            const overcomeRelations = relationsData.relations.filter(r => r.relation_type === 'overcome');
            
            if (generateRelations.length > 0) {
                html += `
                    <div class="relations-group generate-group">
                        <h5><i class="fas fa-arrow-circle-up"></i> 相生关系</h5>
                        <div class="relations-items">
                `;
                generateRelations.forEach(relation => {
                    const strengthBar = Math.round(relation.strength * 100);
                    html += `
                        <div class="relation-item generate">
                            <div class="relation-desc">${relation.description}</div>
                            <div class="strength-bar">
                                <div class="strength-fill generate" style="width: ${strengthBar}%"></div>
                                <span class="strength-text">${strengthBar}%</span>
                            </div>
                        </div>
                    `;
                });
                html += `
                        </div>
                    </div>
                `;
            }
            
            if (overcomeRelations.length > 0) {
                html += `
                    <div class="relations-group overcome-group">
                        <h5><i class="fas fa-arrow-circle-down"></i> 相克关系</h5>
                        <div class="relations-items">
                `;
                overcomeRelations.forEach(relation => {
                    const strengthBar = Math.round(relation.strength * 100);
                    html += `
                        <div class="relation-item overcome">
                            <div class="relation-desc">${relation.description}</div>
                            <div class="strength-bar">
                                <div class="strength-fill overcome" style="width: ${strengthBar}%"></div>
                                <span class="strength-text">${strengthBar}%</span>
                            </div>
                        </div>
                    `;
                });
                html += `
                        </div>
                    </div>
                `;
            }
            
            html += `
                    </div>
                </div>
            `;
        }
        
        html += `
                </div>
            </div>
        `;
        
        return html;
    }

    renderQuestionAnswer(answer) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-question-circle"></i> 针对性建议</h3>
                <div class="content">
                    ${this.formatTextWithLineBreaks(answer)}
                </div>
            </div>
        `;
    }

    renderPracticeSuggestions(suggestions) {
        return `
            <div class="result-item">
                <h3><i class="fas fa-spa"></i> 调候练习建议</h3>
                <div class="content">
                    ${this.formatTextWithLineBreaks(suggestions)}
                </div>
            </div>
        `;
    }

    renderExpertAnalysis(analysis) {
        return `
            <div class="result-item expert-mode">
                <h3><i class="fas fa-microscope"></i> 专家分析详情</h3>
                <div class="content">
                    ${this.formatTextWithLineBreaks(analysis)}
                </div>
            </div>
        `;
    }

    renderExpertData(expertData) {
        if (!expertData) return '';
        
        return `
            <div class="result-item expert-data">
                <h3><i class="fas fa-cog"></i> 技术分析数据</h3>
                <div class="expert-technical-info">
                    <div class="technical-item">
                        <span class="label">规则依据：</span>
                        <span class="value">${expertData.规则依据 || 'N/A'}</span>
                    </div>
                    <div class="technical-item">
                        <span class="label">判定优先级：</span>
                        <span class="value">${(expertData.判定优先级 || []).join(', ')}</span>
                    </div>
                    <div class="technical-item">
                        <span class="label">审计信息：</span>
                        <span class="value">${expertData.审计信息 || 'N/A'}</span>
                    </div>
                </div>
            </div>
        `;
    }

    renderDisclaimer(disclaimer) {
        if (!disclaimer) return '';
        
        return `
            <div class="result-item disclaimer">
                <h3><i class="fas fa-info-circle"></i> 免责声明</h3>
                <div class="disclaimer-content">
                    ${this.formatTextWithLineBreaks(disclaimer)}
                </div>
            </div>
        `;
    }

    formatTextWithLineBreaks(text) {
        if (!text) return '';
        return text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    }

    showResultSection() {
        document.querySelectorAll('.input-section').forEach(section => {
            section.style.display = 'none';
        });
        this.resultSection.style.display = 'block';
    }

    showInputSection(mode) {
        this.resultSection.style.display = 'none';
        this.loading.style.display = 'none';
        this.switchTab(mode);
        
        // 重置表单
        if (this.baziForm) this.baziForm.reset();
        if (this.birthForm) this.birthForm.reset();
        
        this.validateBaziInput();
    }

    async downloadPDF() {
        if (!this.currentAnalysisData) {
            this.showError('没有可下载的分析结果');
            return;
        }

        try {
            const requestData = this.getLastRequestData();
            
            const response = await fetch('/api/v2/generate-pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error('PDF生成失败');
            }

            // 下载文件
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `八字分析报告_${new Date().toISOString().slice(0, 10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
        } catch (error) {
            this.showError('PDF下载失败：' + error.message);
        }
    }

    getLastRequestData() {
        // 从简化表单获取最后的请求数据
        return {
            birth_info: {
                name: this.nameInput?.value || '',
                gender: this.genderInput?.value || '',
                year: parseInt(this.birthYearInput?.value) || 1990,
                month: parseInt(this.birthMonthInput?.value) || 1,
                day: parseInt(this.birthDayInput?.value) || 1,
                hour: parseInt(this.birthHourInput?.value) || 12,
                minute: 0,
                location: this.locationInput?.value || ''
            },
            question: this.questionInput?.value || '',
            mode: this.modeInput?.value || 'general',
            llm_option: this.llmOptionInput?.value || 'local',
            current_age: parseInt(this.currentAgeInput?.value) || 25
        };
    }

    toggleExpertView() {
        this.isExpertView = !this.isExpertView;
        this.toggleExpertBtn.innerHTML = this.isExpertView 
            ? '<i class="fas fa-eye"></i> 简化视图' 
            : '<i class="fas fa-cog"></i> 专家视图';
            
        if (this.currentAnalysisData) {
            this.displayResult(this.currentAnalysisData);
        }
    }

    setupLoadingAnimation() {
        // 预设置加载步骤
        const steps = ['解析八字', '五行统计', '格局判定', '寒燥分析', '病药判定', '大运分析', '智能解读'];
        const stepsContainer = document.querySelector('.loading-steps');
        if (stepsContainer) {
            stepsContainer.innerHTML = steps.map(step => 
                `<div class="step">${step}</div>`
            ).join('');
        }
    }

    showError(message) {
        this.hideLoading();
        alert(`错误: ${message}`);
        this.showInputSection(this.currentMode);
    }

    async showApiSettings() {
        if (this.apiSettingsModal) {
            // 显示模态框
            this.apiSettingsModal.style.display = 'flex';
            
            // 加载当前API状态
            await this.loadApiStatus();
        }
    }
    
    async loadApiStatus() {
        try {
            const response = await fetch('/api/v2/claude-api-status');
            const status = await response.json();
            
            this.updateApiStatusDisplay(status);
        } catch (error) {
            console.error('加载API状态失败:', error);
            this.apiStatusDiv.innerHTML = `
                <div class="status-error">
                    <i class="fas fa-exclamation-triangle"></i> 
                    无法加载API状态
                </div>
            `;
        }
    }
    
    updateApiStatusDisplay(status) {
        let statusHtml = '';
        let statusClass = '';
        
        switch (status.status) {
            case 'configured':
                statusClass = 'status-success';
                statusHtml = `
                    <i class="fas fa-check-circle"></i>
                    <strong>API已配置</strong> - Claude API可以正常使用
                `;
                break;
            case 'not_configured':
                statusClass = 'status-warning';
                statusHtml = `
                    <i class="fas fa-exclamation-circle"></i>
                    <strong>需要配置API Key</strong> - 请输入您的DashScope API Key
                `;
                break;
            default:
                statusClass = 'status-error';
                statusHtml = `
                    <i class="fas fa-times-circle"></i>
                    <strong>API配置错误</strong> - ${status.message || '未知错误'}
                `;
        }
        
        this.apiStatusDiv.innerHTML = `<div class="${statusClass}">${statusHtml}</div>`;
    }
    
    async testApiConnection() {
        const baseUrl = document.getElementById('apiBaseUrl').value;
        const apiKey = document.getElementById('apiKey').value;
        
        if (!apiKey) {
            alert('请先输入API Key');
            return;
        }
        
        this.testApiBtn.disabled = true;
        this.testApiBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 测试中...';
        
        try {
            const response = await fetch('/api/v2/configure-claude-api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    base_url: baseUrl,
                    api_key: apiKey
                })
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                alert('API连接测试成功！');
                this.updateApiStatusDisplay({
                    status: 'configured',
                    message: 'API连接测试成功'
                });
            } else {
                throw new Error(result.detail || '测试失败');
            }
            
        } catch (error) {
            alert('API连接测试失败: ' + error.message);
            console.error('API测试错误:', error);
        } finally {
            this.testApiBtn.disabled = false;
            this.testApiBtn.innerHTML = '<i class="fas fa-vial"></i> 测试连接';
        }
    }
    
    async handleApiConfigSubmit(e) {
        e.preventDefault();
        
        const baseUrl = document.getElementById('apiBaseUrl').value;
        const apiKey = document.getElementById('apiKey').value;
        
        try {
            const response = await fetch('/api/v2/configure-claude-api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    base_url: baseUrl,
                    api_key: apiKey
                })
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                alert('API配置保存成功！');
                this.closeModal();
                // 更新LLM选项的可用性
                this.updateLLMOptionAvailability(true);
            } else {
                throw new Error(result.detail || '配置保存失败');
            }
            
        } catch (error) {
            alert('配置保存失败: ' + error.message);
            console.error('API配置错误:', error);
        }
    }
    
    updateLLMOptionAvailability(isAvailable) {
        if (this.llmOptionInput) {
            const claudeOption = this.llmOptionInput.querySelector('option[value="claude_api"]');
            if (claudeOption) {
                claudeOption.disabled = !isAvailable;
                if (!isAvailable && this.llmOptionInput.value === 'claude_api') {
                    this.llmOptionInput.value = 'local';
                }
            }
        }
    }

    closeModal() {
        if (this.disclaimerModal) {
            this.disclaimerModal.style.display = 'none';
        }
        if (this.apiSettingsModal) {
            this.apiSettingsModal.style.display = 'none';
        }
    }
}

// 全局函数
function showDisclaimer() {
    const modal = document.getElementById('disclaimerModal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new EnhancedBaziApp();
});

// 实用工具函数
const EnhancedUtils = {
    formatDate(date) {
        return new Intl.DateTimeFormat('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(date);
    },
    
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
    },
    
    validateBazi(baziString) {
        const pattern = /^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]\s+[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]\s+[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]\s+[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]$/;
        return pattern.test(baziString.trim());
    }
};