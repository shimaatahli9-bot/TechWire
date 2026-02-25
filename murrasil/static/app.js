let currentTab = 'new';
let currentPage = 1;
let currentArticle = '';

async function api(endpoint, options = {}) {
    const res = await fetch(endpoint, options);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `fixed bottom-4 right-4 px-4 py-3 rounded-lg shadow-lg transform transition-all z-50 ${type === 'success' ? 'bg-green-600' : 'bg-red-600'} text-white`;
    toast.style.transform = 'translateY(0)';
    toast.style.opacity = '1';
    setTimeout(() => {
        toast.style.transform = 'translateY(100%)';
        toast.style.opacity = '0';
    }, 3000);
}

function timeAgo(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);
    if (diff < 60) return 'الآن';
    if (diff < 3600) return `منذ ${Math.floor(diff / 60)} دقيقة`;
    if (diff < 86400) return `منذ ${Math.floor(diff / 3600)} ساعة`;
    return `منذ ${Math.floor(diff / 86400)} يوم`;
}

async function loadCounts() {
    const counts = await api('/api/news/counts');
    document.getElementById('count-new').textContent = counts.new || 0;
    document.getElementById('count-approved').textContent = counts.approved || 0;
    document.getElementById('count-rejected').textContent = counts.rejected || 0;
}

async function loadNews() {
    const container = document.getElementById('news-container');
    const loading = document.getElementById('loading');
    container.innerHTML = '';
    loading.classList.remove('hidden');
    
    try {
        const data = await api(`/api/news?status=${currentTab}&page=${currentPage}`);
        loading.classList.add('hidden');
        
        if (data.news.length === 0) {
            container.innerHTML = '<div class="text-center text-gray-500 py-10">لا توجد أخبار</div>';
            return;
        }
        
        data.news.forEach(item => {
            container.appendChild(createNewsCard(item));
        });
    } catch (e) {
        loading.classList.add('hidden');
        container.innerHTML = `<div class="text-center text-red-500 py-10">خطأ في التحميل: ${e.message}</div>`;
    }
}

function createNewsCard(item) {
    const card = document.createElement('div');
    card.className = 'bg-white rounded-xl shadow-sm p-4 card-enter';
    card.id = `news-${item.id}`;
    
    if (currentTab === 'new') {
        card.innerHTML = `
            <div class="flex items-center gap-2 mb-2">
                <span class="bg-blue-100 text-blue-600 text-xs px-2 py-1 rounded-full">${item.category}</span>
                <span class="text-gray-500 text-sm">${item.source_name}</span>
                <span class="text-gray-400 text-sm mr-auto">${timeAgo(item.fetched_at)}</span>
            </div>
            <h3 class="text-lg font-bold text-gray-800 mb-2">${item.title_ar}</h3>
            <p class="text-gray-600 text-sm mb-4 line-clamp-3">${item.summary_ar}</p>
            <div class="flex gap-2">
                <button onclick="approveNews('${item.id}')" class="flex-1 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition flex items-center justify-center gap-2">
                    ✅ كتابة الخبر
                </button>
                <button onclick="rejectNews('${item.id}')" class="flex-1 bg-red-100 text-red-600 py-2 rounded-lg hover:bg-red-200 transition">
                    ❌ رفض
                </button>
            </div>
        `;
    } else if (currentTab === 'approved') {
        const preview = item.article_ar ? item.article_ar.substring(0, 100) + '...' : '';
        card.innerHTML = `
            <div class="flex items-center gap-2 mb-2">
                <span class="bg-green-100 text-green-600 text-xs px-2 py-1 rounded-full">${item.category}</span>
                <span class="text-gray-500 text-sm">${item.source_name}</span>
                <span class="text-gray-400 text-sm mr-auto">${timeAgo(item.fetched_at)}</span>
            </div>
            <h3 class="text-lg font-bold text-gray-800 mb-2">${item.title_ar}</h3>
            <p class="text-gray-600 text-sm mb-4">${preview}</p>
            <button onclick="showArticle('${item.id}')" class="w-full bg-blue-100 text-blue-600 py-2 rounded-lg hover:bg-blue-200 transition">
                عرض المقال الكامل
            </button>
        `;
    } else {
        card.innerHTML = `
            <div class="flex items-center justify-between">
                <div>
                    <span class="text-gray-500 text-sm">${item.source_name}</span>
                    <h3 class="text-gray-600">${item.title_ar}</h3>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-gray-400 text-sm">${timeAgo(item.fetched_at)}</span>
                    <button onclick="restoreNews('${item.id}')" class="text-blue-600 hover:text-blue-700 text-sm">استعادة</button>
                </div>
            </div>
        `;
    }
    
    return card;
}

async function approveNews(id) {
    const card = document.getElementById(`news-${id}`);
    const btn = card.querySelector('button');
    btn.innerHTML = '<div class="spinner mx-auto"></div>';
    btn.disabled = true;
    
    try {
        const data = await api(`/api/news/${id}/approve`, { method: 'POST' });
        if (data.success) {
            currentArticle = data.article;
            showModal(item.title_ar, data.article);
            card.classList.add('card-exit');
            setTimeout(() => {
                loadNews();
                loadCounts();
            }, 300);
            showToast('تم إنشاء المقال بنجاح');
        }
    } catch (e) {
        btn.innerHTML = '✅ كتابة الخبر';
        btn.disabled = false;
        showToast('فشل في إنشاء المقال', 'error');
    }
}

async function rejectNews(id) {
    const card = document.getElementById(`news-${id}`);
    card.classList.add('card-exit');
    
    try {
        await api(`/api/news/${id}/reject`, { method: 'POST' });
        setTimeout(() => {
            loadNews();
            loadCounts();
        }, 300);
        showToast('تم رفض الخبر');
    } catch (e) {
        card.classList.remove('card-exit');
        showToast('فشل في رفض الخبر', 'error');
    }
}

async function restoreNews(id) {
    try {
        await api(`/api/news/${id}/restore`, { method: 'POST' });
        loadNews();
        loadCounts();
        showToast('تم استعادة الخبر');
    } catch (e) {
        showToast('فشل في الاستعادة', 'error');
    }
}

async function showArticle(id) {
    const data = await api(`/api/news?status=approved`);
    const item = data.news.find(n => n.id === id);
    if (item) {
        currentArticle = item.article_ar;
        showModal(item.title_ar, item.article_ar);
    }
}

function showModal(title, content) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-content').textContent = content;
    document.getElementById('modal-overlay').classList.remove('hidden');
}

function closeModal(e) {
    if (!e || e.target.id === 'modal-overlay') {
        document.getElementById('modal-overlay').classList.add('hidden');
    }
}

function copyArticle() {
    navigator.clipboard.writeText(currentArticle).then(() => {
        showToast('تم نسخ المقال');
    });
}

function switchTab(tab) {
    currentTab = tab;
    currentPage = 1;
    document.querySelectorAll('[id^="tab-"]').forEach(el => el.classList.remove('tab-active'));
    document.getElementById(`tab-${tab}`).classList.add('tab-active');
    loadNews();
}

async function fetchNews() {
    const btn = event.target.closest('button');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="spinner mx-auto"></div>';
    btn.disabled = true;
    
    try {
        const data = await api('/api/news/fetch', { method: 'POST' });
        btn.innerHTML = originalText;
        btn.disabled = false;
        loadNews();
        loadCounts();
        showToast(`تم جلب ${data.new_count} خبر جديد`);
    } catch (e) {
        btn.innerHTML = originalText;
        btn.disabled = false;
        showToast('فشل في جلب الأخبار', 'error');
    }
}

function toggleSettings() {
    const sidebar = document.getElementById('settings-sidebar');
    sidebar.classList.toggle('-translate-x-full');
    if (!sidebar.classList.contains('-translate-x-full')) {
        loadSettings();
        loadSources();
    }
}

async function loadSettings() {
    const settings = await api('/api/settings');
    if (settings.fetch_interval_minutes) {
        document.getElementById('fetch-interval').value = settings.fetch_interval_minutes;
    }
    if (settings.max_news_age_hours) {
        document.getElementById('max-age').value = settings.max_news_age_hours;
    }
    if (settings.ai_model) {
        document.getElementById('ai-model').value = settings.ai_model;
    }
}

async function updateSettings() {
    const settings = {
        fetch_interval_minutes: document.getElementById('fetch-interval').value,
        max_news_age_hours: document.getElementById('max-age').value,
        ai_model: document.getElementById('ai-model').value
    };
    await api('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ settings })
    });
    showToast('تم حفظ الإعدادات');
}

async function loadSources() {
    const data = await api('/api/sources');
    const container = document.getElementById('sources-list');
    container.innerHTML = data.sources.map(s => `
        <div class="flex items-center justify-between bg-gray-50 rounded-lg px-3 py-2">
            <span class="text-sm ${s.enabled ? '' : 'text-gray-400'}">${s.name}</span>
            <div class="flex items-center gap-2">
                <label class="relative inline-flex cursor-pointer">
                    <input type="checkbox" ${s.enabled ? 'checked' : ''} onchange="toggleSource(${s.id}, this.checked)" class="sr-only peer">
                    <div class="w-9 h-5 bg-gray-300 peer-checked:bg-blue-600 rounded-full peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:right-0.5 after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all"></div>
                </label>
                <button onclick="deleteSource(${s.id})" class="text-red-500 hover:text-red-700">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
            </div>
        </div>
    `).join('');
}

async function toggleSource(id, enabled) {
    await api(`/api/sources/${id}?enabled=${enabled}`, { method: 'PUT' });
}

async function deleteSource(id) {
    if (confirm('هل تريد حذف هذا المصدر؟')) {
        await api(`/api/sources/${id}`, { method: 'DELETE' });
        loadSources();
        showToast('تم حذف المصدر');
    }
}

async function addNewSource() {
    const name = document.getElementById('new-source-name').value.trim();
    const url = document.getElementById('new-source-url').value.trim();
    
    if (!name || !url) {
        showToast('يرجى ملء جميع الحقول', 'error');
        return;
    }
    
    await api('/api/sources', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, url })
    });
    
    document.getElementById('new-source-name').value = '';
    document.getElementById('new-source-url').value = '';
    loadSources();
    showToast('تم إضافة المصدر');
}

async function init() {
    await loadCounts();
    await loadNews();
    
    const settings = await api('/api/settings');
    if (settings.last_fetch_time) {
        document.getElementById('last-update').textContent = `آخر تحديث: ${timeAgo(settings.last_fetch_time)}`;
    }
}

init();
