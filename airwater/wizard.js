let wizardStep = 1;
const WIZARD_TOTAL = 3;

function initWizard() {
    const nextBtn = document.getElementById('wizardNext');
    const prevBtn = document.getElementById('wizardPrev');
    if (!nextBtn) return;

    nextBtn.addEventListener('click', () => {
        if (wizardStep < WIZARD_TOTAL) { wizardStep++; updateWizardUI(); }
        else document.getElementById('calculator')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    prevBtn?.addEventListener('click', () => {
        if (wizardStep > 1) { wizardStep--; updateWizardUI(); }
    });

    updateWizardUI();
    window.addEventListener('resize', updateWizardLayout);
    updateWizardLayout();
}

function updateWizardLayout() {
    const wrapper = document.querySelector('.calculator-wrapper');
    const wizard = document.getElementById('calcWizard');
    if (!wrapper || !wizard) return;
    const mobile = window.innerWidth < 768;
    wrapper.classList.toggle('wizard-mode', mobile);
    wizard.style.display = mobile ? 'block' : 'none';
    if (!mobile) {
        document.querySelectorAll('.wizard-step-panel').forEach(p => p.style.display = '');
    } else {
        updateWizardUI();
    }
}

function updateWizardUI() {
    const mobile = window.innerWidth < 768;
    document.querySelectorAll('.wizard-step-panel').forEach(panel => {
        const step = parseInt(panel.dataset.step);
        if (mobile) {
            panel.style.display = step === wizardStep ? 'block' : 'none';
        } else {
            panel.style.display = '';
        }
    });

    document.querySelectorAll('.wizard-dot').forEach(dot => {
        dot.classList.toggle('active', parseInt(dot.dataset.step) <= wizardStep);
    });

    const prev = document.getElementById('wizardPrev');
    const next = document.getElementById('wizardNext');
    if (prev) prev.style.visibility = wizardStep === 1 ? 'hidden' : 'visible';

    const lang = window.currentLang || 'ru';
    const nextTexts = {
        1: { ru: 'Далее: параметры', en: 'Next: parameters', zh: '下一步：参数', es: 'Siguiente: parámetros' },
        2: { ru: 'Результат', en: 'Results', zh: '结果', es: 'Resultados' },
        3: { ru: 'Готово ✓', en: 'Done ✓', zh: '完成 ✓', es: 'Listo ✓' }
    };
    if (next) next.textContent = (nextTexts[wizardStep] || nextTexts[3])[lang] || nextTexts[wizardStep].en;
}

document.addEventListener('DOMContentLoaded', initWizard);
