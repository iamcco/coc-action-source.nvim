# ============================================================================
# FILE: coc-action.py
# AUTHOR: 年糕小豆汤 <ooiss@qq.com>
# License: MIT license
# ============================================================================

from denite import util
from .base import Base
from ..kind.base import Base as BaseKind


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'coc-action'
        self.kind = Kind(vim)

    def define_syntax(self):
        self.vim.command('syntax case ignore')
        self.vim.command(r'syntax match deniteAction_header /\v^.*$/ containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteAction_name /\v^ *[^ ]+ / contained '
                         r'containedin=deniteAction_header')
        self.vim.command(r'syntax match deniteAction_param /\v(\[|\{)[^ ]*(\]|\})/ contained '
                         r'containedin=deniteAction_header')
        self.vim.command(r'syntax match deniteAction_desc /->.*$/ contained '
                         r'containedin=deniteAction_header')

    def highlight(self):
        self.vim.command('highlight default link deniteAction_name Type')
        self.vim.command('highlight default link deniteAction_param Statement')
        self.vim.command('highlight default link deniteAction_desc Comment')

    def gather_candidates(self, context):
        candidata = [{
            'word': 'sourceStat -> get the list of completion source stats for current buffer.',
            'source__action': 'sourceStat',
            'source__arg_type': 'no'
        }, {
            'word': 'refreshSource [{source}] -> refresh all sources or {source} as name of source.',
            'source__action': 'refreshSource',
            'source__arg_type': 'yes'
        }, {
            'word': 'toggleSource {source} -> enable/disable {source}.',
            'source__action': 'toggleSource',
            'source__arg_type': 'yes'
        }, {
            'word': 'diagnosticList -> Get all diagnostic items of current neovim session.',
            'source__action': 'diagnosticList',
            'source__arg_type': 'no'
        }, {
            'word': 'diagnosticInfo -> Get diagnostic info of current buffer',
            'source__action': 'diagnosticInfo',
            'source__arg_type': 'no'
        }, {
            'word': 'jumpDefinition -> jump to definition position of current symbol',
            'source__action': 'jumpDefinition',
            'source__arg_type': 'no'
        }, {
            'word': 'jumpImplementation -> Jump to implementation position of current symbol.',
            'source__action': 'jumpImplementation',
            'source__arg_type': 'no'
        }, {
            'word': 'jumpTypeDefinition -> Jump to type definition position of current symbol.',
            'source__action': 'jumpTypeDefinition',
            'source__arg_type': 'no'
        }, {
            'word': 'jumpReferences -> Jump to references position of current symbol.',
            'source__action': 'jumpReferences',
            'source__arg_type': 'no'
        }, {
            'word': 'doHover -> Show documentation of current word at preview window.',
            'source__action': 'doHover',
            'source__arg_type': 'no'
        }, {
            'word': 'showSignatureHelp -> Echo signature help of current function',
            'source__action': 'showSignatureHelp',
            'source__arg_type': 'no'
        }, {
            'word': 'documentSymbols -> Get symbol list of current document.',
            'source__action': 'documentSymbols',
            'source__arg_type': 'no'
        }, {
            'word': 'rename -> Do rename for symbol under cursor position, user would be prompted for new name.',
            'source__action': 'rename',
            'source__arg_type': 'no'
        }, {
            'word': 'workspaceSymbols -> Search for workspace symbols.',
            'source__action': 'workspaceSymbols',
            'source__arg_type': 'no'
        }, {
            'word': 'services -> Get all services infomation list.',
            'source__action': 'services',
            'source__arg_type': 'no'
        }, {
            'word': 'toggleService {serviceId} -> Start or stop one service, used for |coc-denite-service|',
            'source__action': 'toggleService',
            'source__arg_type': 'yes'
        }, {
            'word': 'format -> Format current buffer using language server.',
            'source__action': 'format',
            'source__arg_type': 'no'
        }, {
            'word': 'codeAction [{mode}] -> prompty for a code action and do it.',
            'source__action': 'codeAction',
            'source__arg_type': 'yes'
        }, {
            'word': 'codeLens -> Open codelens buffer in split window, you can jump (use <CR> by default) and run command (use <d> by default).',
            'source__action': 'codeLens',
            'source__arg_type': 'no'
        }, {
            'word': 'codeLensAction -> Do command from codeLens provider, should only be used in codelens buffer.',
            'source__action': 'codeLensAction',
            'source__arg_type': 'no'
        }, {
            'word': 'commands -> Get available global service command id list of current buffer.',
            'source__action': 'commands',
            'source__arg_type': 'no'
        }, {
            'word': 'runCommand [{name}] -> Run global command provided by language server, if {name} not provided, a prompt of command list is shown for select.',
            'source__action': 'runCommand',
            'source__arg_type': 'yes'
        }]
        return candidata


class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'source'
        self.default_action = 'doaction'

    def action_doaction(self, context):
        target = context['targets'][0]
        action = target['source__action']
        arg_type = target['source__arg_type']
        arg = ''
        if arg_type is 'yes':
            prompt = target['word'].split(' ')[1]
            arg = util.input(self.vim, context, 'Enter args %s: ' % prompt)
        self.vim.call('cocActionSource#call', action, arg)
