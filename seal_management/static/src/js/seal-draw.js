/**
 *公章
 *
 * @param {String} id
 * @param {Object} option
 */
function PSeal(id, option) {
    // 获取 canvas
    this.canvas = document.querySelector(id);
    // 获取 ctx
    this.ctx = this.canvas.getContext('2d');
    // 对 option 进行处理，如果没有传入就为空对象
    option = option || {};
}

PSeal.prototype.saveSealImg = function saveSealImg() {
    return this.canvas.toDataURL();
};

Seal.prototype.saveSealImg = function saveSealImg() {
    return this.canvas.toDataURL();
};

/**
 *公司公章
 *
 * @param {String} id
 * @param {Object} option
 */
function Seal(id, option) {
    PSeal.call(this, id, option);

    /* 用户可配置项 */

    // 印章半径
    this.radius = option.radius || 75;
    // 印章颜色
    this.color = option.color || '#e60021';
    // 字体
    this.fontFamily = option.fontFamily || '宋体';
    // 公司名称
    this.companyName = option.companyName || '青岛国富金融资产交易中心';
    // 印章类型名称
    this.typeName = option.typeName;
    // 类型属性字体大小
    this.typeNameSize = option.typeNameSize || 11;
    // 是否有内边框线
    this.hasInnerLine = option.hasInnerLine;
    // 防伪码
    this.securityCode = option.securityCode;

    /* 默认根据半径进行设置 */

    // 边框线的宽度
    this.lineWidth = 4 / 75 * this.radius;
    // 文字与外边框线的距离
    this.lineTextGap = 0.73;
    // 公司名称字体大小
    this.companyNameFontSize = 16 / 75 * this.radius;
    // 印章类型名称字体大小
    this.typeNameFontSize = this.typeNameSize / 75 * this.radius;
    // 防伪码字体大小
    this.securityCodeFontSize = 0.12 * this.radius;
    // 内边框线的宽度
    this.innerLineWidth = 1 / 75 * this.radius;
    // 字与字之间相差的弧度
    this.step = 0.32;
    // 根据公司名称有多少个字，控制第一个字的起始位置
    this.aStartPos = [0, -0.15, -0.31, -0.5, -0.63, -0.83, -0.95, -1.12, -1.27, -1.44, -1.61, -1.77, -1.93, -2.1, -2.23, -2.4, -2.57, -2.73, -2.89];
    // 起始位置的index
    this.startIndex = this.companyName.length - 1;
    // 起始位置
    this.startPos = this.aStartPos[this.startIndex];

    // 初始化
    this._init();
}

Seal.prototype = Object.create(PSeal.prototype);

Seal.prototype.constructor = Seal;

Seal.prototype._init = function _init() {
    this.canvas.width = this.canvas.height = this.radius * 2;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this._drawOuterLine();
    if (this.hasInnerLine) {
        this._drawInnerLine();
    }
    this._drawStar();
    if (this.companyName) {
        this._drawCompanyName();
    }
    if (this.typeName) {
        this._drawTypeName();
    }
    if (this.securityCode) {
        this._drawSecurityCode();
    }
};

Seal.prototype._drawOuterLine = function _drawOuterLine() {
    this.ctx.save();
    this.ctx.strokeStyle = this.color;
    this.ctx.lineWidth = this.lineWidth;
    this.ctx.beginPath();
    this.ctx.arc(this.radius, this.radius, this.radius - this.lineWidth, 0, Math.PI * 2, true);
    this.ctx.stroke();
    this.ctx.restore();
};

Seal.prototype._drawInnerLine = function _drawInnerLine() {
    this.ctx.save();
    this.ctx.strokeStyle = this.color;
    this.ctx.lineWidth = this.innerLineWidth;
    this.ctx.beginPath();
    this.ctx.arc(this.radius, this.radius, this.radius - this.lineWidth - this.radius / 15, 0, Math.PI * 2, true);
    this.ctx.stroke();
    this.ctx.restore();
};

Seal.prototype._drawStar = function _drawStar() {
    var R = this.radius,
        r = R / 3,
        c = 360 / 5 * Math.PI / 180,
        d = c / 2,
        e = d / 2,
        l = r * Math.sin(e) / Math.sin(d + e),
        lsd = l * Math.sin(d),
        lcd = l * Math.cos(d),
        lsc = l * Math.sin(c),
        lcc = l * Math.cos(c),
        rsc = r * Math.sin(c),
        rcc = r * Math.cos(c),
        rsd = r * Math.sin(d),
        rcd = r * Math.cos(d),
        p0 = [R, 2 / 3 * R],
        p1 = [R + lsd, R - lcd],
        p2 = [R + rsc, R - rcc],
        p3 = [R + lsc, R + lcc],
        p4 = [R + rsd, R + rcd],
        p5 = [R, R + l],
        p6 = [R - rsd, R + rcd],
        p7 = [R - lsc, R + lcc],
        p8 = [R - rsc, R - rcc],
        p9 = [R - lsd, R - lcd],
        aPs = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9];
    this.ctx.save();
    this.ctx.fillStyle = this.color;
    this.ctx.beginPath();
    aPs.forEach(function(item) {
            this.ctx.lineTo(item[0], item[1]);
        }, this)
        // for (var i = 0; i < aPs.length; i++) {
        //   var item = aPs[i];
        //   this.ctx.lineTo(item[0], item[1]);
        // }
    this.ctx.closePath();
    this.ctx.fill();
    this.ctx.restore();
};

Seal.prototype._drawCompanyName = function _drawCompanyName() {
    if (this.companyName.length > 19) {
        throw new RangeError('公司名称最多只能为19个字符！');
    }
    this._drawText(this.companyName, this.companyNameFontSize, false, false);
};

Seal.prototype._drawText = function _drawText(text, fontSize, isTypeName, isSecurityCode) {
    var i, letter;
    this.ctx.save();
    this.ctx.fillStyle = this.color;
    this.ctx.font = 'normal normal bold ' + fontSize + 'px ' + this.fontFamily;
    this.ctx.textBaseline = 'middle';
    if (isTypeName) {
        this.ctx.textAlign = 'center';
    } else {
        this.ctx.textAlign = 'left';
    }
    this.ctx.translate(this.radius, this.radius);
    if (isTypeName) {
        this.ctx.fillText(text, 0, this.radius / 2);
    } else {
        for (i = 0; i < text.length; i++) {
            letter = text[i];
            if (isSecurityCode) {
                this._drawLetter(letter, 0.57 - i * 0.1, -this.securityCodeFontSize / 2, this.radius * 0.8);
            } else {
                this._drawLetter(letter, this.startPos + i * this.step, -fontSize / 2, -this.radius * this.lineTextGap);
            }
        }
    }
    this.ctx.restore();
};

Seal.prototype._drawLetter = function _drawLetter(letter, angle, x, y) {
    this.ctx.save();
    this.ctx.rotate(angle);
    this.ctx.fillText(letter, x, y);
    this.ctx.restore();
};

Seal.prototype._drawTypeName = function _drawTypeName() {
    if (typeof this.typeName !== 'string') {
        throw new TypeError('印章类型名称只能为字符串！');
    }
    this._drawText(this.typeName, this.typeNameFontSize, true, false);
};

Seal.prototype._drawSecurityCode = function _drawSecurityCode() {
    if (typeof this.securityCode !== 'string') {
        throw new TypeError('防伪码只能为字符串！');
    }
    if (this.securityCode.length !== 13) {
        throw new RangeError('防伪码只能为13位！');
    }
    this._drawText(this.securityCode, this.securityCodeFontSize, false, true);
};